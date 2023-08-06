#!/usr/bin/env python3

"""
** Management of the encoding of a multimedia stream based on PyAV. **
----------------------------------------------------------------------
"""


import copy
import fractions
import functools
import itertools
import numbers
import pathlib
import tempfile
import typing

import av
import numpy as np
import tqdm

from movia.core.classes.container import ContainerOutput
from movia.core.classes.frame import Frame
from movia.core.classes.frame_audio import FrameAudio
from movia.core.classes.frame_video import FrameVideo
from movia.core.classes.stream import Stream
from movia.core.classes.stream_audio import StreamAudio
from movia.core.classes.stream_video import StreamVideo
from movia.core.exceptions import MissingStreamError, OutOfTimeRange
from movia.core.generation.audio.noise import GeneratorAudioNoise
from movia.core.generation.video.noise import GeneratorVideoNoise



class ContainerOutputFFMPEG(ContainerOutput):
    """
    ** Allows you to write the output file to disk. **

    Attributes
    ----------
    filename : pathlib.Path
        The absolute path + name of the file to encode (readonly).
    streams_settings : list[dict]
        Information related to each codec (readonly).
    container_settings : dict
        Global container file information (readonly).

    Examples
    --------
    >>> import os
    >>> import tempfile
    >>> from movia.core.filters.basic.truncate import FilterTruncate
    >>> from movia.core.generation.audio.noise import GeneratorAudioNoise
    >>> from movia.core.generation.video.noise import GeneratorVideoNoise
    >>> from movia.core.io.write import ContainerOutputFFMPEG
    >>> _, filename = tempfile.mkstemp(suffix=".mkv")
    >>> streams_settings = [{"codec": "mp3", "rate": 44100}, {"codec": "h264", "rate": 24}]
    >>> streams = FilterTruncate(
    ...     (GeneratorAudioNoise.default().out_streams + GeneratorVideoNoise.default().out_streams),
    ...     1,
    ... ).out_streams
    >>> ContainerOutputFFMPEG(streams, filename, streams_settings=streams_settings).write()
    >>> os.remove(filename)
    >>>
    """

    def __init__(self,
        in_streams: typing.Iterable[Stream],
        filename: typing.Union[str, bytes, pathlib.Path],
        streams_settings: typing.Iterable[dict],
        container_settings: dict=None,
    ):
        """
        Parameters
        ----------
        in_streams : typing.Iterable[Stream]
            The ordered video or audio streams to be encoded.
            For more information, please refer to initializator of
            ``movia.core.classes.container.ContainerOutput``.
        filename : pathlike
            Path to the file to be encoded.
        streams_settings : typing.Iterable[dict]
            These are the encoding parameters associated with each stream.
            They contain all the information about the codecs.
            For video au audio streams, here is the format to follow:
                {
                    "codec": str, # name of the codec or encoding library (ex h264 or mp3)
                    "rate": numbers.Real or str,
                        # The framerate or samplerate in Hz (ex "30000/1001" or 44100)
                    "options": dict, # (optional) option for codec (ex {"crf": 23})
                    "bit_rate": int, # (optional) the flow in bytes/s (ex 800000)
                    "pix_fmt": str, # (optional) the pixel format (ex "yuv420p")
                    # all pic_fmt in av.codec.Codec("libx264", "w").video_formats
                }
        container_settings : dict, optional
            Global container file information.
            must contain the following fields:
                {
                    "format": str or None, # specific format to use, defaults to autodect
                    "options": dict, # options to pass to the container and all streams
                    "container_options": dict, # options to pass to the container
                }
        """
        super().__init__(in_streams)

        filename = pathlib.Path(filename)
        assert filename.parent.exists(), filename
        assert not filename.is_dir(), filename
        self._filename = filename

        if container_settings is None:
            container_settings = {}
        assert isinstance(container_settings, dict), container_settings.__class__.__name__
        assert isinstance(container_settings.get("format", None), (str, type(None)))
        assert isinstance(container_settings.get("options", {}), dict)
        assert isinstance(container_settings.get("container_options", {}), dict)
        self._container_settings = copy.deepcopy(container_settings)

        streams_settings = list(streams_settings)
        assert all(isinstance(s, dict) for s in streams_settings), streams_settings
        assert len(streams_settings) == len(self.in_streams)
        for settings in streams_settings:
            assert "codec" in settings, "missing the 'codec' key"
            assert isinstance(settings["codec"], str), settings["codec"].__class__.__name__
            assert "rate" in settings, "missing the 'rate' key"
            if isinstance(settings["rate"], str):
                settings["rate"] = fractions.Fraction(settings["rate"])
            assert isinstance(settings["rate"], numbers.Number)
            assert settings["rate"] > 0
        self._streams_settings = streams_settings

    @classmethod
    def default(cls):
        audio_stream = GeneratorAudioNoise.default().out_streams[0]
        video_stream = GeneratorVideoNoise.default().out_streams[0]
        in_streams = [audio_stream, video_stream]
        _, filename = tempfile.mkstemp(suffix=".mkv")
        streams_settings = [{"codec": "mp3", "rate": 44100}, {"codec": "h264", "rate": 24}]
        return cls(in_streams, filename, streams_settings)

    def getstate(self) -> dict:
        # convertion fraction to str for jsonisable
        streams_settings = self.streams_settings
        for settings in streams_settings:
            if not isinstance(settings["rate"], (int, float)):
                settings["rate"] = str(settings["rate"])
        # get the rest
        return {
            "filename": str(self.filename),
            "streams_settings": streams_settings,
            "container_settings": self.container_settings,
        }

    def setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        keys = {"filename", "streams_settings", "container_settings"}
        assert set(state) == keys, set(state)-keys
        ContainerOutputFFMPEG.__init__(self, in_streams, **state)

    @property
    def filename(self) -> pathlib.Path:
        """
        ** The absolute path + name of the file to encode. **
        """
        return self._filename

    @property
    def streams_settings(self) -> list[dict]:
        """
        ** Information related to each codec. **
        """
        return copy.deepcopy(self._streams_settings)

    @property
    def container_settings(self) -> dict:
        """
        ** Global container file information. **
        """
        return {
            "format": self._container_settings.get("format", None),
            "options": self._container_settings.get("options", {}),
            "container_options": self._container_settings.get("container_options", {}),
        }

    def write(self):
        """
        ** Encodes the streams and writes the file. **
        """
        # container initialisation
        with av.open(
            str(self.filename),
            mode="w",
            format=self.container_settings["format"],
            options=self.container_settings["options"],
            container_options=self.container_settings["container_options"],
        ) as container_av:

            # streams initialisation
            streams_av_video = []
            streams_av_audio = []
            for stream, settings in zip(self.in_streams, self.streams_settings):
                if isinstance(stream, StreamVideo):
                    stream_av = container_av.add_stream(settings["codec"], settings["rate"])
                    streams_av_video.append(stream_av)
                elif isinstance(stream, StreamAudio):
                    stream_av = container_av.add_stream(settings["codec"], settings["rate"])
                    streams_av_audio.append(stream_av)
                else:
                    raise TypeError(
                        "only video and audio streams are accepted, "
                        f"not {stream.__class__.__name__}"
                    )

            # display avancement
            with tqdm.tqdm(
                desc=f"Encoding {self.filename.name}",
                total=float(max(s.beginning + s.duration for s in self.in_streams)),
                dynamic_ncols=True,
                bar_format="{l_bar}{bar}| {n:.2f}s/{total:.2f}s [{elapsed}<{remaining}]",
                smoothing=0.1,
            ) as progress_bar:

                # encode
                rates = [settings["rate"] for settings in self.streams_settings]
                for index, frame in global_scheduler(list(self.in_streams), rates):
                    if isinstance(frame, FrameVideo):
                        frame = frame_video_to_av(frame)
                        stream_av = streams_av_video[index]
                    elif isinstance(frame, FrameAudio):
                        frame = frame_audio_to_av(frame)
                        stream_av = streams_av_audio[index]
                    else:
                        raise TypeError(
                            "only video and audio frame are accepted, "
                            f"not {frame.__class__.__name__}"
                        )
                    container_av.mux(stream_av.encode(frame))
                    progress_bar.update(frame.time - progress_bar.n)
                for stream_av in itertools.chain(streams_av_video, streams_av_audio):
                    container_av.mux(stream_av.encode()) # flush buffer
                progress_bar.update(progress_bar.total - progress_bar.n)


def _raise_missing_stream_error(func):
    """
    ** Raises MissingStreamError if the func yields nothing. **
    """
    @functools.wraps(func)
    def generator(*args, **kwargs):
        empty = True
        for res in func(*args, **kwargs):
            empty = False
            yield res
        if empty:
            raise MissingStreamError("no frame is present in any of the streams")
    return generator

def audio_scheduler(
    streams: list[StreamAudio],
    samplerates: list[numbers.Integral],
    start_time: numbers.Real=0,
    duration: numbers.Real=0.5,
    **_,
) -> typing.Iterable[tuple[int, FrameAudio]]:
    """
    ** Order and create audio frames. **

    Parameters
    ----------
    streams : list[movia.core.classes.stream_audio.StreamAudio]
        The list of different audio streams has been ordered.
    samplerate : list[numbers.Real]
        The sampling frequency of the different input streams.
    start_time : numbers.Real
        Approximate time of the first frame.
    duration : numbers.Real
        The duration of each frame in seconds.

    Yields
    ------
    index : int
        The index of the concerned stream in the order of the provided list.
    frame : av.audio.frame.AudioFrame
        The future frame of the stream considerer.
        The ``time`` attribute is guaranteed to be monotonic.

    Examples
    --------
    >>> from movia.core.generation.audio.noise import GeneratorAudioNoise
    >>> from movia.core.filters.basic.truncate import FilterTruncate
    >>> from movia.core.io.write import audio_scheduler
    >>> stream_1 = FilterTruncate(GeneratorAudioNoise.default().out_streams, 2).out_streams[0]
    >>> stream_2 = FilterTruncate(GeneratorAudioNoise.default().out_streams, 2.5).out_streams[0]
    >>> streams = [stream_1, stream_2]
    >>> samplerates = [44100, 16000]
    >>>
    >>> for index, frame in audio_scheduler(streams, samplerates):
    ...     index, float(frame.time), frame.samples
    ...
    (0, 0.0, 22050)
    (1, 0.0, 8000)
    (0, 0.5, 22050)
    (1, 0.5, 8000)
    (0, 1.0, 22050)
    (1, 1.0, 8000)
    (0, 1.5, 22050)
    (1, 1.5, 8000)
    (1, 2.0, 8000)
    >>> for index, frame in audio_scheduler(streams, samplerates, start_time=2):
    ...     index, float(frame.time), frame.samples
    ...
    (1, 2.0, 8000)
    >>> for index, frame in audio_scheduler(streams, samplerates, start_time=1.75, duration=0.25):
    ...     index, float(frame.time), frame.samples
    ...
    (0, 1.75, 11025)
    (1, 1.75, 4000)
    (1, 2.0, 4000)
    (1, 2.25, 4000)
    >>> for index, frame in audio_scheduler(streams, samplerates, duration=1.5):
    ...     index, float(frame.time), frame.samples
    ...
    (0, 0.0, 66150)
    (1, 0.0, 24000)
    (0, 1.5, 22050)
    (1, 1.5, 16000)
    >>> list(audio_scheduler(streams, samplerates, start_time=3))
    []
    >>>
    """
    assert isinstance(streams, list), streams.__class__.__name__
    assert all(isinstance(s, StreamAudio) for s in streams), streams
    assert isinstance(samplerates, list), streams.__class__.__name__
    assert all(isinstance(s, numbers.Integral) for s in samplerates), samplerates
    assert all(s > 0 for s in samplerates), samplerates
    assert isinstance(start_time, numbers.Real), start_time.__class__.__name__
    assert start_time >= 0, start_time
    assert isinstance(duration, numbers.Real), duration.__class__.__name__
    duration = float(duration)
    assert duration > 0, duration
    assert len(streams) == len(samplerates)

    is_exausted = [False for _ in range(len(streams))] # allows to mark fully iterated flows.
    for frame_index in itertools.count(start=round(start_time/duration)):
        if all(is_exausted):
            break
        for index in (i for i, e in enumerate(is_exausted.copy()) if not e):
            timestamp = frame_index * duration
            if not (samples := round(duration * samplerates[index])): # case after end
                is_exausted[index] = True
                continue
            if timestamp < streams[index].beginning: # case start befor beginning
                end = timestamp + fractions.Fraction(samples, samplerates[index])
                samples = round((end - streams[index].beginning) * samplerates[index])
                if samples <= 0:
                    continue
                timestamp = streams[index].beginning
            try:
                frame = streams[index].snapshot(timestamp, samplerates[index], samples)
            except OutOfTimeRange:
                is_exausted[index] = True
                if (samples := round(
                    (streams[index].beginning + streams[index].duration - timestamp)
                    * samplerates[index]
                )) <= 0:
                    continue
                frame = streams[index].snapshot(timestamp, samplerates[index], samples)
            yield index, frame


@_raise_missing_stream_error
def global_scheduler(
    streams: list[Stream],
    rates: list[numbers.Real],
    **kwargs: dict,
) -> typing.Iterable[tuple[int, Frame]]:
    """
    ** Assigns in chronological order the frames of all flows. **

    Parameters
    ----------
    streams : list[movia.core.classes.stream.Stream]
        Audio or video streams.
    rates : list[numbers.Real]
        The frame rate for video streams and the sample rate for audio streams.
    **kwargs : dict
        Transmitted to the functions
        ``movia.core.io.write.audio_scheduler`` and ``movia.core.io.write.video_scheduler``.

    Yields
    ------
    index : int
        The relative number of the stream.
    frame_av : av.frame.Frame
        The (PyAv) video or audio frame.

    Raises
    ------
    movia.core.exceptions.MissingStreamError
        If no frame are yielded.
    """
    assert isinstance(streams, list), streams.__class__.__name__
    assert all(isinstance(s, Stream) for s in streams), streams
    assert isinstance(rates, list), rates.__class__.__name__
    assert all(isinstance(r, numbers.Real) for r in rates), rates
    assert len(streams) == len(rates)

    buffer_video = [] # fifo for video frames
    buffer_audio = [] # fifo for audio frames

    video = iter(video_scheduler(
        [s for s in streams if isinstance(s, StreamVideo)],
        [r for r, s in zip(rates, streams) if isinstance(s, StreamVideo)],
        **kwargs,
    ))
    audio = iter(audio_scheduler(
        [s for s in streams if isinstance(s, StreamAudio)],
        [getattr(s, "samplerate", r) for r, s in zip(rates, streams) if isinstance(s, StreamAudio)],
        **kwargs,
    ))

    while buffer_video is not None and buffer_audio is not None:
        # completes the empty buffers
        if len(buffer_video) == 0:
            try:
                buffer_video.append(next(video))
            except StopIteration:
                yield from itertools.chain(buffer_audio, audio)
                break
        if len(buffer_audio) == 0:
            try:
                buffer_audio.append(next(audio))
            except StopIteration:
                yield from itertools.chain(buffer_video, video)
                break

        # selection of the oldest
        if buffer_video[0][1].time <= buffer_audio[0][1].time:
            yield buffer_video.pop(0)
        else:
            yield buffer_audio.pop(0)


def frame_audio_to_av(frame_audio: FrameAudio) -> av.audio.frame.AudioFrame:
    """
    ** Converts a FrameAudio movia into a av frame for encodage. **

    Parameters
    ----------
    frame_audio : movia.core.classes.frame_audio.FrameAudio
        The torch frame to cast.

    Returns
    -------
    av_frame : av.audio.frame.audioFrame
        The equivalent av audio frame containing a similar audio signal.

    Examples
    --------
    >>> from movia.core.classes.frame_audio import FrameAudio
    >>> from movia.core.io.write import frame_audio_to_av
    >>>
    >>> frame_audio_to_av(FrameAudio(10, 44100, 1, 1024)) # doctest: +ELLIPSIS
    <av.AudioFrame 0, pts=441000, 1024 samples at 44100Hz, mono, flt at ...>
    >>> frame_audio_to_av(FrameAudio(10, 44100, 2, 1024)) # doctest: +ELLIPSIS
    <av.AudioFrame 0, pts=441000, 1024 samples at 44100Hz, stereo, flt at ...>
    >>>
    """
    assert isinstance(frame_audio, FrameAudio), frame_audio.__class__.__name__
    frame_np = frame_audio.numpy(force=True)
    frame_np = frame_np.astype(np.float32)
    frame_np = np.ascontiguousarray(frame_np) # fix ValueError: ndarray is not C-contiguous
    frame_av = av.audio.frame.AudioFrame.from_ndarray(
        np.expand_dims(frame_np.ravel(order="F"), 0),
        format="flt",
        layout=frame_audio.channels,
    )
    frame_av.rate = frame_audio.rate
    frame_av.time_base = fractions.Fraction(1, frame_audio.rate)
    frame_av.pts = round(frame_audio.time * frame_audio.rate)
    return frame_av


def frame_video_to_av(frame_video: FrameVideo) -> av.video.frame.VideoFrame:
    """
    ** Converts a FrameVideo movia into a av frame for the encodage. **

    Parameters
    ----------
    frame_video : movia.core.classes.frame_video.FrameVideo
        The torch frame video to cast.

    Returns
    -------
    av_frame : av.video.frame.VideoFrame
        The equivalent av video frame containing the similar image in format bgr24.

    Examples
    --------
    >>> from movia.core.classes.frame_video import FrameVideo
    >>> from movia.core.io.write import frame_video_to_av
    >>>
    >>> frame_video_to_av(FrameVideo(10, 480, 720, 3)) # doctest: +ELLIPSIS
    <av.VideoFrame #0, pts=3003000 bgr24 720x480 at ...>
    >>> frame_video_to_av(FrameVideo(10, 480, 720, 1)) # doctest: +ELLIPSIS
    <av.VideoFrame #0, pts=3003000 bgr24 720x480 at ...>
    >>> frame_video_to_av(FrameVideo(10, 480, 720, 4)) # doctest: +ELLIPSIS
    <av.VideoFrame #0, pts=3003000 bgr24 720x480 at ...>
    >>>
    """
    assert isinstance(frame_video, FrameVideo), frame_video.__class__.__name__
    frame_av = av.video.frame.VideoFrame.from_ndarray(frame_video.to_numpy_bgr(), format="bgr24")
    frame_av.time_base = fractions.Fraction(1, 300300) # ppcm 1001, 25, 30, 60
    frame_av.pts = round(frame_video.time / frame_av.time_base)
    return frame_av


def video_scheduler(
    streams: list[StreamVideo],
    out_fps: list[numbers.Real],
    start_time: numbers.Real=0,
    **_,
) -> typing.Iterable[tuple[int, FrameVideo]]:
    """
    ** Order the packets from several video streams. **

    Gives up frames until all streams have raised the OutOfTimeRange exception.

    Parameters
    ----------
    streams : list[movia.core.classes.stream_video.StreamVideo]
        The list of different video streams has been ordered.
    out_fps : list[numbers.Real]
        The encoding frequencies for each of the output video streams.

    Yields
    ------
    index : int
        The index of the concerned stream in the order of the provided list.
    frame : av.video.frame.VideoFrame
        The future frame of the stream considerer.
        The ``time`` attribute is guaranteed to be monotonic.
    start_time : numbers.Real
        Approximate time of the first frame.

    Examples
    --------
    >>> from movia.core.generation.video.noise import GeneratorVideoNoise
    >>> from movia.core.filters.basic.truncate import FilterTruncate
    >>> from movia.core.io.write import video_scheduler
    >>> stream_1 = FilterTruncate(GeneratorVideoNoise.default().out_streams, 0.1).out_streams[0]
    >>> stream_2 = FilterTruncate(GeneratorVideoNoise.default().out_streams, 0.25).out_streams[0]
    >>> streams = [stream_1, stream_2]
    >>> out_fps = [30, 24]
    >>>
    >>> for index, frame in video_scheduler(streams, out_fps):
    ...     index, round(frame.time, 3)
    ...
    (0, 0.0)
    (1, 0.0)
    (0, 0.033)
    (1, 0.042)
    (0, 0.067)
    (1, 0.083)
    (1, 0.125)
    (1, 0.167)
    (1, 0.208)
    >>> for index, frame in video_scheduler(streams, out_fps, start_time=0.1):
    ...     index, round(frame.time, 3)
    ...
    (1, 0.083)
    (1, 0.125)
    (1, 0.167)
    (1, 0.208)
    >>> list(video_scheduler(streams, out_fps, start_time=0.25))
    []
    >>>
    """
    assert isinstance(streams, list), streams.__class__.__name__
    assert all(isinstance(s, StreamVideo) for s in streams), streams
    assert isinstance(out_fps, list), out_fps.__class__.__name__
    assert all(isinstance(f, numbers.Real) for f in out_fps), out_fps
    assert all(f > 0 for f in out_fps), out_fps # avoid division by 0
    assert isinstance(start_time, numbers.Real), start_time.__class__.__name__
    assert start_time >= 0, start_time
    assert len(streams) == len(out_fps)

    steps = [round(start_time*fps) for fps in out_fps] # avoids accumulating inaccuracies
    buffer = [[] for _ in range(len(streams))] # fifo for each stream, None when terminated

    while any(fifo is not None for fifo in buffer):
        try:
            index = buffer.index([]) # search position of empty stream
        except ValueError: # in case you have to yield a frame
            time2index = [
                (frames[0].time, ind) for ind, frames in enumerate(buffer) if frames is not None
            ]
            min_time = min(t for t, _ in time2index)
            index = [ind for time, ind in time2index if time == min_time].pop(0)
            yield index, buffer[index].pop(0)
        else: # in case you need to recover a new frame
            try:
                buffer[index].append(streams[index].snapshot(steps[index]/out_fps[index]))
            except OutOfTimeRange:
                if steps[index]/out_fps[index] < streams[index].beginning: # case stream comes later
                    black_frame = streams[index].snapshot(np.nan)
                    black_frame = FrameVideo(steps[index]/out_fps[index], black_frame)
                    buffer[index].append(black_frame) # padding with black frames
                else:
                    buffer[index] = None
            steps[index] += 1
