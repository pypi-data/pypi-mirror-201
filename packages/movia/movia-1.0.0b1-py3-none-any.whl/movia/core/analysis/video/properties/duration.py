#!/usr/bin/env python3

"""
** Finds the duration of a video stream. **
-------------------------------------------

This allows not only the characteristics of the files but also the tags if there are any.
"""

import collections
import pathlib
import typing

import cv2 # pip install opencv-contrib-python-headless

from movia.core.exceptions import MissingStreamError, MissingInformation
from movia.core.analysis.video.properties.parser import (_check_pathexists_index,
    _decode_duration_frames_ffmpeg, _mix_and_check, _parse_ffprobe_res)



def _decode_duration_ffmpeg(filename: str, index: int) -> float:
    """
    ** Extract the duration by the complete decoding of the stream. **

    Slow but 100% accurate method.

    Examples
    --------
    >>> from movia.core.analysis.video.properties.duration import _decode_duration_ffmpeg
    >>> _decode_duration_ffmpeg("movia/examples/video.mp4", 0)
    16.0
    >>>
    """
    duration, _ = _decode_duration_frames_ffmpeg(filename, index)
    return duration

def _decode_duration_cv2(filename: str, index: int) -> float:
    """
    ** Extract the duration by the complete decoding of the stream. **

    Slow but 100% accurate method.

    Examples
    --------
    >>> from movia.core.analysis.video.properties.duration import _decode_duration_cv2
    >>> _decode_duration_cv2("movia/examples/video.mp4", 0)
    16.0
    >>>
    """
    cap = cv2.VideoCapture(filename, index)
    if not cap.isOpened():
        raise MissingStreamError(f"impossible to open '{filename}' stream {index} with 'cv2'")
    if (fps := float(cap.get(cv2.CAP_PROP_FPS))) <= 0:
        one_over_fps = 0
    else:
        one_over_fps = 1 / fps
    duration = .0
    while True:
        duration = (1e-3 * float(cap.get(cv2.CAP_PROP_POS_MSEC))) or (duration + one_over_fps)
        if not cap.read()[0]:
            break
    cap.release()
    if not duration:
        raise MissingStreamError(f"'cv2' did not find duration '{filename}' stream {index}")
    return round(duration + one_over_fps, 3)

def _estimate_duration_ffmpeg(filename: str, index: int) -> float:
    """
    ** Extract the duration from the metadata. **

    Very fast method but inaccurate. It doesn't work all the time.

    Examples
    --------
    >>> from movia.core.analysis.video.properties.duration import _estimate_duration_ffmpeg
    >>> _estimate_duration_ffmpeg("movia/examples/video.mp4", 0)
    16.0
    >>>
    """
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", f"v:{index}",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        filename,
    ]
    duration = _parse_ffprobe_res(cmd, filename, index)
    try:
        duration = float(duration)
    except ValueError as err:
        raise MissingInformation(
            f"'ffprobe' did not get a correct duration in '{filename}' stream {index}"
        ) from err
    if duration <= 0:
        raise MissingInformation(
            f"'ffprobe' finds a duration of {duration} in '{filename}' stream {index}"
        )
    return duration

def _estimate_duration_cv2(filename: str, index: int) -> float:
    """
    ** Extract the duration from the metadata. **

    Very fast method but inaccurate. It doesn't work all the time.

    Examples
    --------
    >>> from movia.core.analysis.video.properties.duration import _estimate_duration_cv2
    >>> _estimate_duration_cv2("movia/examples/video.mp4", 0)
    16.0
    >>>
    """
    cap = cv2.VideoCapture(filename, index)
    if not cap.isOpened():
        raise MissingStreamError(f"impossible to open '{filename}' stream {index} with 'cv2'")
    frames = float(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = float(cap.get(cv2.CAP_PROP_FPS))
    duration = frames / fps if fps and frames else 0
    cap.release()
    if duration <= 0:
        raise MissingInformation(
            f"'cv2' does not detect any duration in '{filename}' stream {index}"
        )
    return duration

def get_duration(
    filename: typing.Union[str, bytes, pathlib.Path],
    index: int=0,
    *,
    backend: typing.Union[None, str]=None,
    accurate: bool=False,
) -> float:
    """
    ** Recovers the total duration of a video stream. **

    The duration includes the display time o the last frame.

    Parameters
    ----------
    filename : pathlike
        The pathlike of the file containing a video stream.
    index : int
        The index of the video stream being considered,
        by default the first stream encountered is selected.
    backend : str, optional
        - None (default) : Try to read the stream by trying differents backends.
        - 'ffmpeg' : Uses the modules ``pip3 install ffmpeg-python``
            which are using the ``ffmpeg`` program in the background.
        - 'cv2' : Uses the module ``pip3 install opencv-contrib-python-headless``.
    accurate : boolean, optional
        If True, recovers the duration by fully decoding all the frames in the video.
        It is very accurate but very slow. If False (default),
        first tries to get the duration from the file metadata.
        It's not accurate but very fast.

    Returns
    -------
    duration : float
        The total duration of the considerated video stream.

    Raises
    ------
    MissingStreamError
        If the file does not contain a playable video stream.
    MissingInformation
        If the information is unavailable.
    """
    _check_pathexists_index(filename, index)

    return _mix_and_check(
        backend, accurate, (str(pathlib.Path(filename)), index),
        collections.OrderedDict([
            (_estimate_duration_ffmpeg, {"accurate": False, "backend": "ffmpeg"}),
            (_estimate_duration_cv2, {"accurate": False, "backend": "cv2"}),
            (_decode_duration_ffmpeg, {"accurate": True, "backend": "ffmpeg"}),
            (_decode_duration_cv2, {"accurate": True, "backend": "cv2"}),
        ])
    )
