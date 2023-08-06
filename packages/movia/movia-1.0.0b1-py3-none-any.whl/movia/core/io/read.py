#!/usr/bin/env python3

"""
** Decodes the streams of a multimedia file based on ffmpeg. **
---------------------------------------------------------------
"""


import fractions
import numbers
import pathlib
import typing

import av
import numpy as np
import torch

from movia.core.analysis.streams import get_streams_type
from movia.core.analysis.video.properties.framerate import get_fps
from movia.core.analysis.video.properties.nb_frames import get_nb_frames
from movia.core.classes.container import ContainerInput
from movia.core.classes.frame_audio import FrameAudio
from movia.core.classes.frame_video import FrameVideo
from movia.core.classes.stream import Stream
from movia.core.classes.stream_audio import StreamAudio
from movia.core.classes.stream_video import StreamVideo
from movia.core.exceptions import MissingInformation, MissingStreamError, OutOfTimeRange
from movia.utils import get_project_root



class ContainerInputFFMPEG(ContainerInput):
    """
    ** Allows to decode a multimedia file with ffmpeg. **

    Attributes
    ----------
    av_kwargs : dict[str]
        The parameters passed to ``av.open``.
    filename : pathlib.Path
        The path to the physical file that contains the extracted video stream (readonly).

    Notes
    -----
    In order to avoid the folowing error :
        ``av.error.InvalidDataError: [Errno 1094995529] Invalid data found when processing input;
        last error log: [libdav1d] Error parsing OBU data``
    Which happens when reading a multi-stream file sparingly, The instances of
    ``av.container.InputContainer`` are new for each stream.

    Examples
    --------
    >>> from movia.core.io.read import ContainerInputFFMPEG
    >>> with ContainerInputFFMPEG("movia/examples/intro.mkv") as container:
    ...     for stream in container.out_streams:
    ...         if stream.type == "video":
    ...             stream.snapshot(0).shape
    ...         elif stream.type == "audio":
    ...             stream.snapshot(0, 2, 3)
    ...
    (720, 1280, 3)
    (360, 640, 3)
    FrameAudio([[    nan,  0.1453, -0.3620],
                [    nan,  0.0450,  0.0421]], metadata=(Fraction(0, 1), 2))
    FrameAudio([[    nan,  0.1140, -0.2884]], metadata=(Fraction(0, 1), 2))
    >>>
    """

    def __init__(self, filename: typing.Union[str, bytes, pathlib.Path], **av_kwargs):
        """
        Parameters
        ----------
        filename : pathlike
            Path to the file to be decoded.
        **av_kwargs : dict
            Directly transmitted to ``av.open``.

            * ``"format" (str)``: Specific format to use. Defaults to autodect.
            * ``"options" (dict)``: Options to pass to the container and all streams.
            * ``"container_options" (dict)``: Options to pass to the container.
            * ``"stream_options" (list)``: Options to pass to each stream.
            * ``"metadata_encoding" (str)``: Encoding to use when reading or writing file metadata.
                Defaults to "utf-8".
            * ``"metadata_errors" (str)``: Specifies how to handle encoding errors;
                behaves like str.encode parameter. Defaults to "strict".
            * ``"buffer_size" (int)``: Size of buffer for Python input/output operations in bytes.
                Honored only when file is a file-like object. Defaults to 32768 (32k).
            * ``"timeout" (float or tuple)``: How many seconds to wait for data before giving up,
                as a float, or a (open timeout, read timeout) tuple.
        """
        filename = pathlib.Path(filename)
        assert filename.is_file(), filename

        self._filename = filename
        self._av_kwargs = av_kwargs # need for compilation
        self._av_kwargs["options"] = self._av_kwargs.get("options", {})
        self._av_kwargs["container_options"] = self._av_kwargs.get("container_options", {})

        out_streams = [self._init_out_stream(s_t) for s_t in get_streams_type(filename)]
        super().__init__(out_streams)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def _init_out_stream(self, stream_type: str) -> Stream:
        if (
            stream_class := (
                {"audio": _StreamAudioFFMPEG, "video": _StreamVideoFFMPEG}.get(stream_type, None)
            )
        ) is None:
            raise ValueError(f"only 'audio' and 'video' stream is supproted, not {stream_type}")
        return stream_class(self)

    @classmethod
    def default(cls):
        return cls(get_project_root() / "examples" / "intro.mkv")

    def getstate(self) -> dict:
        return {
            "filename": str(self.filename),
            "av_kwargs": self.av_kwargs,
        }

    def setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        keys = {"filename", "av_kwargs"}
        assert set(state) == keys, set(state)-keys
        ContainerInputFFMPEG.__init__(self, state["filename"], **state["av_kwargs"])

    def close(self):
        """
        ** Close the file. **
        """
        for stream in self.out_streams:
            stream.close()

    @property
    def av_kwargs(self) -> dict[str]:
        """
        ** The parameters passed to ``av.open``. **
        """
        return self._av_kwargs

    @property
    def filename(self) -> pathlib.Path:
        """
        ** The path to the physical file that contains the extracted video stream. **
        """
        return self._filename


class _StreamAudioFFMPEG(StreamAudio):
    """
    Attributes
    ----------
    duration : numbers.Real
        The exact duration of the stream (readonly).
        This date corresponds to the end of the last sample.
    metadata : dict
        The metadata associated with this stream (readonly).
    rate : int
        The frequency in Hz of the samples (readonly).
    time_base : fractions.Fraction
        The unit of time (in fractional seconds) in which timestamps are expressed (readonly).
    """

    is_time_continuous = False

    def __init__(self, node: ContainerInputFFMPEG):
        """
        Parameters
        ----------
        node : movia.core.io.read.ContainerInputFFMPEG
            Simply allows to keep the graph structure.
        """
        assert isinstance(node, ContainerInputFFMPEG), node.__class__.__name__
        super().__init__(node)

        self._av_container = None
        self._frame_iter = None # we can't recreate it every time because we lose the last frames
        self._array_buff = [None, None]
        self._prec_frame = self._next_frame = None
        self._duration = None

    def __iter__(self):
        """
        ** Yields all frames and array of this stream starting from the current position. **
        """
        if self._prec_frame is None:
            self._update_prec_next()
        yield self._prec_frame, self._extract_array_prec()
        if self._next_frame is not self._prec_frame:
            yield self._next_frame, self._extract_array_next()
        while True:
            try:
                yield self._update_prec_next(), self._extract_array_next()
            except OutOfTimeRange:
                break

    def _extract_array_next(self):
        if self._array_buff[1] is None:
            self._array_buff[1] = _clip_convert(self._next_frame.to_ndarray(format="bgr24"))
        return self._array_buff[1]

    def _extract_array_prec(self):
        if self._array_buff[0] is None:
            if self._prec_frame is None:
                self._update_prec_next()
            self._array_buff[0] = _clip_convert(self._prec_frame.to_ndarray(format="bgr24"))
        return self._array_buff[0]

    def _seek_backward(self, position: numbers.Real):
        """
        ** Moves backwards in the file. **

        This method guarantees to move before the required position.
        If this is not possible, we move to the very beginning of the file.
        """
        if self._prec_frame is None:
            self._update_prec_next()

        # adjusted displacement
        seek_request = max(0, int(
            (position - self._prec_frame.samples/self._prec_frame.rate)
            / self._prec_frame.time_base
        ))
        self.av_container.seek(
            seek_request,
            backward=True, # if there is not a keyframe at the given offset
            stream=self.av_container.streams[self.index]
        )
        self._frame_iter = None # takes into account the new position
        self._array_buff = [None, None]
        self._prec_frame = self._next_frame = None
        self._update_prec_next()

        # verification and rough adjustment
        if seek_request != 0:
            if position > _frame_dates(self._prec_frame)[0]:
                self._seek_backward(0)

    def _seek_forward(self, position: numbers.Real):
        """
        ** Moves forwardwards in the file. **

        The displacement, if any, can be very approximate.
        """
        self.av_container.seek(
            max(0, round(position)),
            backward=True, # if there is not a keyframe at the given offset
            stream=self.av_container.streams[self.index]
        )

    def _snapshot(self, timestamp: fractions.Fraction, rate: int, samples: int) -> FrameAudio:
        # resample if needeed
        if samples != 1 and rate != self.rate:
            frame = self._snapshot(timestamp, rate=self.rate, samples=round(samples*self.rate/rate))
            indexs = torch.arange(samples, dtype=torch.float64)
            indexs *= self.rate / rate
            indexs = torch.round(indexs, out=indexs).to(dtype=torch.int64)
            indexs = torch.clamp(indexs, max=frame.samples-1, out=indexs) # solve IndexError
            frame = FrameAudio(timestamp, rate, frame[:, indexs])
            return frame

        # seeking if nescessary
        self.seek(timestamp) # seeks only for backward or big forward jump

        # retrive and decode reference samples
        t_max = timestamp + fractions.Fraction(samples - 1, rate) # starting time of the last sample
        references = [] # (is_corrupt, (t_start, t_end_including_last_sample_duration), rate, array)
        for frame, array in self:
            references.append((frame.is_corrupt, _frame_dates(frame), frame.rate, array))
            if references[-1][1][1] > t_max + self.time_base: # a sample covers [t0, t0+dt[
                break
        else: # if the last frame is reached
            if t_max >= references[-1][1][1]:
                raise OutOfTimeRange(
                    f"there is no audio frame at timestamp {t_max} "
                    f"(need timestamp < {_frame_dates(self._next_frame)[1]})"
                )

        # verifications
        if any(r != self.rate for _, _, r, _ in references):
            raise NotImplementedError(f"rate ({self.rate}) doesn't match the frames")

        # create the new empty audio frame
        dtypes = {ref[3].dtype.type for ref in references}
        dtypes = {
            {np.float16: torch.float16, np.float32: torch.float32, np.float64: torch.float64}[t]
            for t in dtypes
        }
        dtypes = sorted(
            dtypes, key=lambda t: {torch.float16: 2, torch.float32: 1, torch.float64: 0}
        )
        dtype = dtypes[0]
        frame = FrameAudio(
            timestamp, rate, torch.full((self.channels, samples), torch.nan, dtype=dtype)
        )

        # positionning of each slices
        for ref in references:
            if ref[0]: # if frame is corrupt, live nan
                continue
            pos = round((ref[1][0] - timestamp) * self.rate) # index of the frame
            buff = ref[3]
            if pos < 0:
                buff = buff[:, -pos:]
                pos = 0
            if pos+buff.shape[1] > samples: # if ref to long
                buff = buff[:, :max(0, samples-pos)]
            if buff.shape[1]:
                frame[:, pos:pos+buff.shape[1]] = torch.from_numpy(buff)
        return frame

    def _update_prec_next(self) -> av.audio.frame.AudioFrame:
        """
        ** Iterates on the next audio frame. **

        Returns
        -------
        _next_frame : av.audio.frame.AudioFrame
            The newly decoded frame.

        Raises
        ------
        OutOfTimeRange
            If the last audio frame has already been reached.
        """
        self._prec_frame, self._array_buff[0] = self._next_frame, self._array_buff[1]
        try:
            self._next_frame = next(self.frame_iter)
        except StopIteration as err:
            raise OutOfTimeRange("there is no audio frame left to read") from err
        self._array_buff[1] = None
        if self._prec_frame is None:
            self._prec_frame = self._next_frame
        return self._next_frame

    @property
    def av_container(self) -> av.container.Container:
        """
        ** Allows to read the file at the last moment. **
        """
        if self._av_container is None:
            self._av_container = av.open(str(self.node.filename), "r", **self.node.av_kwargs)
        return self._av_container

    @property
    def channels(self) -> int:
        """
        ** The number of channels in this audio stream. **

        Examples
        --------
        >>> from movia.core.io.read import ContainerInputFFMPEG
        >>> with ContainerInputFFMPEG("movia/examples/audio.ogg") as container:
        ...     (stream,) = container.out_streams
        ...     stream.channels
        ...
        1
        >>>
        """
        return self.av_container.streams[self.index].codec_context.channels

    def close(self):
        """
        ** Close the file. **
        """
        if self._av_container is not None:
            self._av_container.close()

    @property
    def duration(self) -> numbers.Real:
        """
        ** The exact duration in seconds. **

        Examples
        --------
        >>> from movia.core.io.read import ContainerInputFFMPEG
        >>> with ContainerInputFFMPEG("movia/examples/audio.ogg") as container:
        ...     (stream,) = container.out_streams
        ...     stream.duration
        ...
        Fraction(16, 1)
        >>>
        """
        if self._duration is not None:
            return self._duration

        while True:
            try:
                self._update_prec_next()
            except OutOfTimeRange:
                break
        self._duration = _frame_dates(self._next_frame)[1]
        return self._duration

    @property
    def frame_iter(self) -> typing.Iterable:
        """
        ** Allows to read the file at the last moment. **
        """
        if self._frame_iter is None:
            self._frame_iter = iter(
                self.av_container.decode(self.av_container.streams[self.index])
            )
        return self._frame_iter

    @property
    def metadata(self) -> int:
        """
        ** The metadata associated with this stream. **

        Examples
        --------
        >>> from movia.core.io.read import ContainerInputFFMPEG
        >>> with ContainerInputFFMPEG("movia/examples/audio.ogg") as container:
        ...     (stream,) = container.out_streams
        ...     stream.metadata
        ...
        {'encoder': 'Lavc59.37.100 libvorbis'}
        >>>
        """
        return self.av_container.streams[self.index].metadata

    @property
    def rate(self) -> int:
        """
        ** The frequency of the samples. **

        Examples
        --------
        >>> from movia.core.io.read import ContainerInputFFMPEG
        >>> with ContainerInputFFMPEG("movia/examples/audio.ogg") as container:
        ...     (stream,) = container.out_streams
        ...     stream.rate
        ...
        16000
        >>>
        """
        return self.av_container.streams[self.index].codec_context.rate

    def seek(self, position: numbers.Real):
        """
        ** Moves into the file. **

        If you are already well placed, this has no effect.
        Allows backward even a little bit, but only jump forward if the jump is big enough.
        """
        assert isinstance(position, numbers.Real), position.__class__.__name__
        if self._prec_frame is None:
            self._update_prec_next()

        # case need to seek
        if (
            position - 10 > (
                _frame_dates(self._next_frame)[0]
                + fractions.Fraction(self._next_frame.samples, self._next_frame.rate)
            )
        ): # take a leap forward (jump > 10 s)
            self._seek_forward(position) # very approximative
        if position < _frame_dates(self._prec_frame)[0]:
            self._seek_backward(position) # guaranteed to be before

        # fine adjustment
        while (
            _frame_dates(self._next_frame)[0]
            + fractions.Fraction(self._next_frame.samples, self._next_frame.rate)
            < position
        ):
            self._update_prec_next()

    @property
    def time_base(self) -> fractions.Fraction:
        """
        ** The unit of time (in fractional seconds) in which timestamps are expressed. **

        Examples
        --------
        >>> from movia.core.io.read import ContainerInputFFMPEG
        >>> with ContainerInputFFMPEG("movia/examples/audio.ogg") as container:
        ...     (stream,) = container.out_streams
        ...     stream.time_base
        ...
        Fraction(1, 16000)
        >>>
        """
        return self.av_container.streams[self.index].time_base


class _StreamVideoFFMPEG(StreamVideo):
    """
    Attributes
    ----------
    duration : numbers.Real
        The exact duration of the stream (readonly).
        This date corresponds to the end of the last frame.
    framerate : numbers.Real
        Theoretical image frequency in the metadata (readonly).
    nb_frames : int
        The exact number of frames present in this stream (readonly).
    time_base : fractions.Fraction
        The unit of time (in fractional seconds) in which timestamps are expressed (readonly).
    """

    is_space_continuous = False
    is_time_continuous = False

    def __init__(self, node: ContainerInputFFMPEG):
        """
        Parameters
        ----------
        node : movia.core.io.read.ContainerInputFFMPEG
            Simply allows to keep the graph structure.
        """
        assert isinstance(node, ContainerInputFFMPEG), node.__class__.__name__
        super().__init__(node)

        self._av_container = None
        self._key_times = None
        self._frame_iter = None # we can't recreate it every time because we lose the last frames
        self._prec_frame = self._next_frame = None
        self._duration = None

    def __iter__(self):
        """
        ** Yields all frames of this stream starting from the current position. **
        """
        if self._next_frame is None:
            self._update_prec_next()
        yield self._next_frame
        while True:
            try:
                yield self._update_prec_next()
            except OutOfTimeRange:
                break

    def _snapshot_av(self, timestamp: float) -> av.video.frame.VideoFrame:
        # ideal case (select the nearest)
        if self._prec_frame is None:
            self._update_prec_next()
        if self._prec_frame.time <= timestamp <= self._next_frame.time:
            delta_prec = timestamp - self._prec_frame.time
            delta_next = self._next_frame.time - timestamp
            return self._prec_frame if delta_prec <= delta_next else self._next_frame

        key_prec, key_next = _born(self.key_times, timestamp)
        if key_prec is None:
            raise OutOfTimeRange(f"there is no frame at timestamp {timestamp} (need >= {key_next})")

        # case need seek (backward or big displacement)
        if (
            self._prec_frame.time > timestamp # back to the past
            or self._next_frame.time < key_prec - .5 # take a leap forward (jump > 500 ms)
        ):
            self.av_container.seek(
                1 + int(key_prec / self.av_container.streams[self.index].time_base),
                backward=True, # if there is not a keyframe at the given offset
                any_frame=False, # seek to any frame, not just a keyframe
                stream=self.av_container.streams[self.index]
            )
            self._frame_iter = None # takes into account the new position

        # decoding until reaching the right frame
        try:
            while timestamp > self._update_prec_next().time:
                continue
        except OutOfTimeRange as err: # management of the time overrun of the last frame
            if timestamp >= self._next_frame.time + 1/self.framerate:
                raise err
            return self._next_frame
        return self._snapshot_av(timestamp)

    def _snapshot(self, timestamp: float) -> FrameVideo:
        frame_av = self._snapshot_av(timestamp)
        return FrameVideo(frame_av.time, frame_av.to_ndarray(format="bgr24"))

    def _update_prec_next(self) -> av.video.frame.VideoFrame:
        """
        ** Iterates on the next frame. **

        Raises
        ------
        OutOfTimeRange
            If the last frame has already been reached.
        """
        self._prec_frame = self._next_frame
        try:
            self._next_frame = next(self.frame_iter)
        except StopIteration as err:
            raise OutOfTimeRange("there is no frame left to read") from err
        if self._prec_frame is None:
            self._prec_frame = self._next_frame
        return self._next_frame

    @property
    def av_container(self) -> av.container.Container:
        """
        ** Allows to read the file at the last moment. **
        """
        if self._av_container is None:
            self._av_container = av.open(str(self.node.filename), "r", **self.node.av_kwargs)
        return self._av_container

    def close(self):
        """
        ** Close the file. **
        """
        if self._av_container is not None:
            self._av_container.close()

    @property
    def duration(self) -> numbers.Real:
        """
        ** The exact duration in seconds. **

        Examples
        --------
        >>> from movia.core.io.read import ContainerInputFFMPEG
        >>> with ContainerInputFFMPEG("movia/examples/video.mp4") as container:
        ...     (stream,) = container.out_streams
        ...     stream.duration
        ...
        16.0
        >>>
        """
        if self._duration is not None:
            return self._duration
        self._snapshot_av(self.key_times[-1])
        self._duration = self.key_times[-1]
        for frame in self:
            self._duration = frame.time
        assert self._duration is not None
        self._duration += 1/self.framerate # duration of the last frame
        return self._duration

    @property
    def frame_iter(self) -> typing.Iterable:
        """
        ** Allows to read the file at the last moment. **
        """
        if self._frame_iter is None:
            self._frame_iter = iter(
                self.av_container.decode(self.av_container.streams[self.index])
            )
        return self._frame_iter

    @property
    def framerate(self) -> numbers.Real:
        """
        ** Theoretical image frequency in the metadata. **
        """
        rel_index = [
            i for i, s_ in enumerate(
                s for s in self.node.out_streams if isinstance(s, _StreamVideoFFMPEG)
            ) if s_ is self
        ].pop()
        return get_fps(self.node.filename, rel_index)

    @property
    def height(self) -> int:
        return self.av_container.streams[self.index].height

    @property
    def key_times(self) -> np.ndarray[np.float32]:
        """
        ** Allows to read the file at the last moment. **
        """
        if self._key_times is None:
            self._key_times = np.fromiter(
                (
                    frame.time for frame in _extract_key_frames(
                        self.av_container.streams[self.index]
                    )
                ),
                dtype=np.float32,
            )
            if len(self._key_times) == 0:
                raise MissingStreamError(
                    f"can not decode any frames of {self.node.filename} stream {self.index}"
                )
            if np.any(np.isnan(self._key_times)):
                raise MissingInformation("the timestamp is not known for all keyframes")
        return self._key_times

    @property
    def nb_frames(self) -> int:
        """
        ** The exact number of frames present in this stream. **
        """
        rel_index = [
            i for i, s_ in enumerate(
                s for s in self.node.out_streams if isinstance(s, _StreamVideoFFMPEG)
            ) if s_ is self
        ].pop()
        return get_nb_frames(self.node.filename, rel_index, accurate=True)

    @property
    def time_base(self) -> fractions.Fraction:
        """
        ** The unit of time (in fractional seconds) in which timestamps are expressed. **

        Examples
        --------
        >>> from movia.core.io.read import ContainerInputFFMPEG
        >>> with ContainerInputFFMPEG("movia/examples/video.mp4") as container:
        ...     (stream,) = container.out_streams
        ...     stream.time_base
        ...
        Fraction(1, 12800)
        >>>
        """
        return self.av_container.streams[self.index].time_base

    @property
    def width(self) -> int:
        return self.av_container.streams[self.index].width


def _born(refs, val):
    """
    ** Search the 2 values that encadre the number. **

    The interval sought is the upper one.

    Parameters
    ----------
    refs : np.ndarray
        The list in ascending order of key values.
    val : numbers.Real
        The value to be placed among the other values.

    Examples
    --------
    >>> import numpy as np
    >>> from movia.core.io.read import _born
    >>> _born(np.array([0, 2]), -1)
    (None, 0)
    >>> _born(np.array([0, 2]), 0)
    (0, 2)
    >>> _born(np.array([0, 2]), 1)
    (0, 2)
    >>> _born(np.array([0, 2]), 2)
    (2, None)
    >>> _born(np.array([0, 2]), 3)
    (2, None)
    >>> _born(np.array([0]), -1)
    (None, 0)
    >>> _born(np.array([0]), 0)
    (0, None)
    >>> _born(np.array([0]), 1)
    (0, None)
    >>>
    """
    if val < refs[0]:
        return None, refs[0]
    if val >= refs[-1]:
        return refs[-1], None
    ind_sup = np.argmin(refs <= val)
    return refs[ind_sup-1], refs[ind_sup]


def _clip_convert(audio_samples: np.ndarray[numbers.Real]) -> np.ndarray[numbers.Real]:
    """
    ** Converts sound samples into float between -1 and 1. **

    Minimizes copying and reallocations.

    Examples
    --------
    >>> import numpy as np
    >>> from movia.core.io.read import _clip_convert
    >>> _clip_convert(np.array([-1.5, -1.0, -.5, .5, 1.0, 1.5], dtype=np.float64))
    array([-1. , -1. , -0.5,  0.5,  1. ,  1. ])
    >>> _clip_convert(np.array([-1.5, -1.0, -.5, .5, 1.0, 1.5], dtype=np.float32))
    array([-1. , -1. , -0.5,  0.5,  1. ,  1. ], dtype=float32)
    >>> _clip_convert(np.array([-1.5, -1.0, -.5, .5, 1.0, 1.5], dtype=np.float16))
    array([-1. , -1. , -0.5,  0.5,  1. ,  1. ], dtype=float16)
    >>> _clip_convert(np.array([-2147483648, -1073741824, 1073741824, 2147483647], dtype=np.int32))
    array([-1. , -0.5,  0.5,  1. ])
    >>> _clip_convert(np.array([-32768, -16384, 16384, 32767], dtype=np.int16))
    array([-1.        , -0.49999237,  0.50002289,  1.        ])
    >>> _clip_convert(np.array([0, 64, 192, 255], dtype=np.uint8))
    array([-1.        , -0.49803922,  0.50588235,  1.        ])
    >>>
    """
    assert isinstance(audio_samples, np.ndarray), audio_samples.__class__.__name__
    if issubclass(audio_samples.dtype.type, numbers.Integral):
        iinfo = np.iinfo(audio_samples.dtype)
        audio_samples = audio_samples.astype(np.float64)
        audio_samples -= .5*np.float64(iinfo.min + iinfo.max)
        audio_samples /= .5*np.float64(iinfo.max - iinfo.min)
    else:
        np.clip(audio_samples, -1, 1, out=audio_samples)
    return audio_samples


def _extract_key_frames(av_stream):
    """
    ** Extract the list of key frames. **

    Examples
    --------
    >>> import av
    >>> from movia.core.io.read import _extract_key_frames
    >>> with av.open("movia/examples/video.mp4") as av_container:
    ...     key_frames = list(_extract_key_frames(av_container.streams.video[0]))
    ...
    >>> [f.time for f in key_frames]
    [0.0, 10.0]
    >>>
    """
    assert isinstance(av_stream, av.video.stream.VideoStream), av_stream.__class__.__name__
    av_stream.container.seek(0, backward=True, any_frame=False, stream=av_stream)
    av_stream.codec_context.skip_frame = "NONKEY"
    yield from av_stream.container.decode(av_stream)
    av_stream.container.seek(0, backward=True, any_frame=False, stream=av_stream)
    av_stream.codec_context.skip_frame = "DEFAULT"


def _frame_dates(frame: av.frame.Frame) -> tuple[numbers.Real, numbers.Real]:
    """
    ** Returns the accurate time interval of the given frame. **

    Include the duration of the last frame / sample.

    Examples
    --------
    >>> import av
    >>> from movia.core.io.read import _frame_dates
    >>> with av.open("movia/examples/video.mp4") as av_container:
    ...     frame = next(av_container.decode(av_container.streams.video[0]))
    ...     _frame_dates(frame)
    ...
    (Fraction(0, 1), Fraction(0, 1))
    >>> with av.open("movia/examples/audio.ogg") as av_container:
    ...     frame = next(av_container.decode(av_container.streams.audio[0]))
    ...     _frame_dates(frame)
    ...
    (Fraction(0, 1), Fraction(4, 125))
    >>>
    """
    assert isinstance(frame, av.frame.Frame), frame.__class__.__name__

    if (pts := frame.pts) is None or (time_base := frame.time_base) is None:
        start_time = frame.time
    else:
        start_time = pts * time_base
    if isinstance(frame, av.audio.frame.AudioFrame):
        stop_time = start_time + fractions.Fraction(frame.samples, frame.rate)
        return start_time, stop_time
    return start_time, start_time
