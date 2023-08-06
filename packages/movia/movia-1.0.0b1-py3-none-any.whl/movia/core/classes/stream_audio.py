#!/usr/bin/env python3

"""
** Defines the structure of an abstract audio stream. **
--------------------------------------------------------
"""

import abc
import fractions
import logging
import numbers
import typing

import torch

from movia.core.classes.filter import Filter
from movia.core.classes.frame_audio import FrameAudio
from movia.core.classes.stream import Stream, StreamWrapper
from movia.core.exceptions import OutOfTimeRange



class StreamAudio(Stream):
    """
    ** Representation of any audio stream. **

    Attributes
    ----------
    channels : int
        The number of tracks (readonly).
    """

    @property
    @abc.abstractmethod
    def channels(self) -> int:
        """
        ** The number of channels in this audio stream. **
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _snapshot(self, timestamp: fractions.Fraction, rate: int, samples: int) -> FrameAudio:
        raise NotImplementedError

    def snapshot(self,
        timestamp: numbers.Real,
        rate: typing.Optional[numbers.Integral]=None,
        samples: numbers.Integral=1,
    ) -> FrameAudio:
        """
        ** Extract the closest values to the requested date. **

        Parameters
        ----------
        timestamp : numbers.Real
            The absolute time expressed in seconds, not relative to the beginning of the audio.
            Is the instant of the first sample of the returned frame.
        rate : numbers.Integral, optional
            If samples == 1, this argument is ignored. Otherwise is the samplerate of the frame.
            If provide and samples != 1, allows to deduce the timestamps of the non 0 samples.
            If non provide and samples != 1, try to call the `rate` attribute of the stream.
        samples : numbers.Integral, default=1
            The number of audio samples per channels to catch.

        Returns
        -------
        samples : FrameAudio
            Audio samples corresponding to the times provided.
            This vector is of shape (nbr_channels, *timestamp_shape).
            The values are between -1 and 1.

        Raises
        ------
        movia.core.exception.OutOfTimeRange
            If we try to read a sample at a negative time or after the end of the stream.
        AttributeError
            If the `rate` attribute has to be defined but is not provides or deductable.
        """
        # verifications on input
        assert isinstance(samples, numbers.Integral), samples.__class__.__name__
        samples = int(samples)
        assert samples > 0, samples
        if rate is None:
            if samples != 1:
                if (rate := getattr(self, "rate", None)) is None:
                    raise ValueError("rate attribute has to be provide")
            else:
                rate = 1 # ignore default unused stupid value
        assert isinstance(rate, numbers.Integral), rate.__class__.__name__
        rate = int(rate)
        assert rate > 0, rate
        assert isinstance(timestamp, numbers.Real), timestamp.__class__.__name__
        try:
            timestamp = fractions.Fraction(timestamp)
        except ValueError as err: # case nan
            raise NotImplementedError("nan case not implemented") from err
        if timestamp < 0:
            raise OutOfTimeRange(f"there is no audio frame at timestamp {timestamp} (need >= 0)")

        # extract samples
        frame = self._snapshot(timestamp, rate, samples)

        # result verification
        assert isinstance(frame, FrameAudio), frame.__class__.__name__
        min_val, max_val = torch.aminmax(frame)
        if min_val.item() < -1 or max_val.item() > 1:
            logging.warning(
                "saturated samples detected min %f max %f", min_val.item(), max_val.item()
            )
        return frame

    @property
    def type(self) -> str:
        return "audio"

class StreamAudioWrapper(StreamWrapper, StreamAudio):
    """
    ** Allows to dynamically transfer the methods of an instanced audio stream. **

    This can be very useful for implementing filters.
    """

    def __init__(self, node: Filter, index: numbers.Integral):
        """
        Parameters
        ----------
        filter : movia.core.classes.filter.Filter
            The parent node, transmitted to ``movia.core.classes.stream.Stream``.
        index : number.Integral
            The index of the audio stream among all the input streams of the ``node``.
            0 for the first, 1 for the second ...
        """
        assert isinstance(node, Filter), node.__class__.__name__
        assert len(node.in_streams) > index, f"only {len(node.in_streams)} streams, no {index}"
        assert isinstance(node.in_streams[index], StreamAudio), "the stream must be audio type"
        super().__init__(node, index)

    def _snapshot(self, timestamp: fractions.Fraction, rate: int, samples: int) -> FrameAudio:
        return self.stream._snapshot(timestamp)

    @property
    def channels(self) -> int:
        return self.stream.channels
