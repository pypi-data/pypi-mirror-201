#!/usr/bin/env python3

"""
** Smartly choose the framerate of a video stream. **
-----------------------------------------------------
"""


import fractions
import numbers

from movia.core.classes.stream_video import StreamVideo



def find_optimal_video_rate(
    stream: StreamVideo, default: numbers.Real=fractions.Fraction(30000, 1001)
) -> numbers.Real:
    """
    ** Finds the optimal sampling rate for a given video stream. **

    Parameters
    ----------
    stream : movia.core.classes.stream_video.StreamVideo
        The video stream that we want to find the optimal fps.
    default : numbers.real, optional
        Final value in case the optimal value has not been found.

    Returns
    -------
    framerate : numbers.Real
        The framerate (maximum) that allows to minimize / cancel the loss of information,
        (minimum) and avoids an excess of frame that does not bring more information.
    """
    assert isinstance(stream, StreamVideo), stream.__class__.__name__
    assert isinstance(default, numbers.Real), default.__class__.__name__
    assert default > 0, default

    return default
