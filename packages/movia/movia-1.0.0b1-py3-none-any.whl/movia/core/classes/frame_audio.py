#!/usr/bin/env python3

"""
** Defines the structure an audio frame. **
-------------------------------------------
"""


import numbers

from movia.core.classes.frame import Frame



class FrameAudio(Frame):
    """
    ** An audio sample packet with time information. **

    Behaves like a torch tensor of shape (nbr_channels, samples).
    The shape is consistent with pyav and torchaudio.
    Values are supposed to be between -1 and 1.

    Parameters
    ----------
    channels : int
        The numbers of channels (readonly).
    rate : int
        The frequency of the samples in Hz (readonly).
    samples : int
        The number of samples per channels (readonly).
    time : numbers.Real
        The time of the first sample of the frame in second (readonly).
    """

    def __new__(cls, time: numbers.Real, rate: numbers.Integral, *args, **kwargs):
        assert isinstance(time, numbers.Real), time.__class__.__name__
        assert isinstance(rate, numbers.Integral), rate.__class__.__name__
        assert rate > 0, rate
        metadata = (time, int(rate))
        frame = super().__new__(cls, *args, metadata=metadata, **kwargs)
        assert frame.ndim == 2, frame.shape
        assert frame.shape[0] > 0, frame.shape
        assert frame.dtype.is_floating_point, frame.dtype
        return frame

    @property
    def channels(self) -> int:
        """
        ** The numbers of channels. **

        Examples
        --------
        >>> from movia.core.classes.frame_audio import FrameAudio
        >>> FrameAudio(0, 44100, 2, 10).channels
        2
        >>>
        """
        return self.shape[0]

    @property
    def rate(self) -> int:
        """
        ** The frequency of the samples in Hz. **

        Examples
        --------
        >>> from movia.core.classes.frame_audio import FrameAudio
        >>> FrameAudio(0, 44100, 2, 1).rate
        44100
        >>>
        """
        return self.metadata[1]

    @property
    def samples(self) -> int:
        """
        ** The number of samples per channels. **

        Examples
        --------
        >>> from movia.core.classes.frame_audio import FrameAudio
        >>> FrameAudio(0, 44100, 2, 10).samples
        10
        >>>
        """
        return self.shape[1]

    @property
    def time(self) -> numbers.Real:
        """
        ** The time of the first sample of the frame in second. **

        Examples
        --------
        >>> from movia.core.classes.frame_audio import FrameAudio
        >>> FrameAudio(0, 44100, 2, 1).time
        0
        >>>
        """
        return self.metadata[0]
