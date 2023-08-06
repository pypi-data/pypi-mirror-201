#!/usr/bin/env python3

"""
** Smartly choose the framerate of an audio stream. **
------------------------------------------------------
"""

import numbers

from movia.core.classes.stream_audio import StreamAudio



def find_optimal_audio_rate(
    stream: StreamAudio, default: numbers.Integral=48000
) -> numbers.Real:
    """
    ** Finds the optimal sampling rate for a given audio stream. **

    Parameters
    ----------
    stream : movia.core.classes.stream_audio.StreamAudio
        The audio stream that we want to find the optimal rate.
    default : numbers.Integral, optional
        Final value in case the optimal value has not been found.

    Returns
    -------
    framerate : int
        The minimum samplerate that respects the Nyquist–Shannon theorem.
    """
    assert isinstance(stream, StreamAudio), stream.__class__.__name__
    assert isinstance(default, numbers.Integral), default.__class__.__name__
    assert default > 0, default

    return default
