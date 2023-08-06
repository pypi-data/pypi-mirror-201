#!/usr/bin/env python3

"""
** Allows you to temporarily translate a sequence. **
-----------------------------------------------------
"""

import fractions
import numbers
import typing

from movia.core.classes.filter import Filter
from movia.core.classes.frame_audio import FrameAudio
from movia.core.classes.frame_video import FrameVideo
from movia.core.classes.stream import Stream
from movia.core.classes.stream_audio import StreamAudioWrapper
from movia.core.classes.stream_video import StreamVideoWrapper
from movia.core.generation.audio.noise import GeneratorAudioNoise
from movia.core.generation.video.noise import GeneratorVideoNoise



class FilterTranslate(Filter):
    """
    ** Change the beginning time of a stream. **

    Attributes
    ----------
    delay : fractions.Fraction
        The delay append to the original begenning time of the stream (readonly).
        a positive value indicates that the output flow is later than the input flow.
    """

    def __init__(self, in_streams: typing.Iterable[Stream], delay: numbers.Real):
        """
        Parameters
        ----------
        in_streams : typing.Iterable[Stream]
            Forwarded to ``movia.core.classes.filter.Filter``.
        delay : numbers.Real
            The temporal translation value to aply at the output stream.
        """
        assert hasattr(in_streams, "__iter__"), in_streams.__class__.__name__
        in_streams = tuple(in_streams)
        assert all(isinstance(stream, Stream) for stream in in_streams), \
            [stream.__class__.__name__ for stream in in_streams]
        assert isinstance(delay, numbers.Real), delay.__class__.__name__

        self._delay = fractions.Fraction(delay)
        super().__init__(in_streams, in_streams)
        super().__init__(
            in_streams,
            [
                (
                    {"audio": _StreamAudioTranslate, "video": _StreamVideoTranslate}
                )[in_stream.type](self, index) for index, in_stream in enumerate(in_streams)
            ]
        )

    @classmethod
    def default(cls):
        audio_stream = GeneratorAudioNoise.default().out_streams[0]
        video_stream = GeneratorVideoNoise.default().out_streams[0]
        return cls([audio_stream, video_stream], 0)

    @property
    def delay(self) -> fractions.Fraction:
        """
        ** The delay append to the original begenning time of the stream. **
        """
        return self._delay

    def getstate(self) -> dict:
        return {"delay": str(self.delay)}

    def setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        assert set(state) == {"delay"}, set(state)-{"delay"}
        FilterTranslate.__init__(self, in_streams, fractions.Fraction(state["delay"]))


class _StreamAudioTranslate(StreamAudioWrapper):
    """
    ** translate an audio stream from a certain delay. **
    """

    def _snapshot(self, timestamp: fractions.Fraction, rate: int, samples: int) -> FrameAudio:
        timestamp = timestamp - self.node.delay
        return self.stream.snapshot(timestamp, rate, samples) # not _snapshot for t < 0 verif

    @property
    def beginning(self) -> numbers.Real:
        return self.stream.beginning + self.node.delay


class _StreamVideoTranslate(StreamVideoWrapper):
    """
    ** translate a video stream from a certain delay. **
    """

    def _snapshot(self, timestamp: float) -> FrameVideo:
        frame = self.stream.snapshot(timestamp - self.node.delay) # not _snapshot for t < 0 verif
        frame = FrameVideo(frame.time + self.node.delay, frame) # copy
        return frame

    @property
    def beginning(self) -> numbers.Real:
        return self.stream.beginning + self.node.delay
