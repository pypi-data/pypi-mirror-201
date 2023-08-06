#!/usr/bin/env python3

"""
** Finds the average frame rate of a video stream. **
-----------------------------------------------------

This information is collected in the metadata of the file.
Its access is fast but its value is not always accurate.
Especially since the framerate is not always constant within the same stream.
"""

import fractions
import numbers
import pathlib
import re
import typing

import cv2 # pip install opencv-contrib-python-headless

from movia.core.exceptions import MissingStreamError, MissingInformation
from movia.core.analysis.video.properties.parser import _parse_ffprobe_res



def _estimate_fps_cv2(filename: str, index: int) -> float:
    """
    ** Retrieves via cv2, the metadata concerning the fps. **

    This function is fast because it reads only the header of the file.

    Examples
    --------
    >>> from movia.core.analysis.video.properties.framerate import _estimate_fps_cv2
    >>> _estimate_fps_cv2("movia/examples/video.mp4", 0)
    25.0
    >>>
    """
    cap = cv2.VideoCapture(filename, index)
    if not cap.isOpened():
        raise MissingStreamError(f"impossible to open '{filename}' stream {index} with 'cv2'")
    fps = float(cap.get(cv2.CAP_PROP_FPS))
    cap.release()
    if fps <= 0:
        raise MissingInformation(f"'cv2' finds an fps of {fps} in '{filename}' stream {index}")
    return fps


def _estimate_fps_ffmpeg(filename: str, index: int) -> fractions.Fraction:
    """
    ** Retrieves via ffmpeg, the metadata concerning the fps. **

    This function is fast because it reads only the header of the file.

    ffprobe -v quiet -print_format json -show_streams -select_streams v:0 video.mp4

    Examples
    --------
    >>> from movia.core.analysis.video.properties.framerate import _estimate_fps_ffmpeg
    >>> _estimate_fps_ffmpeg("movia/examples/video.mp4", 0)
    Fraction(25, 1)
    >>>
    """
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", f"v:{index}", "-show_entries", "stream=r_frame_rate,avg_frame_rate",
        "-of", "default=nokey=1:noprint_wrappers=1",
        filename,
    ]
    fps_str = _parse_ffprobe_res(cmd, filename, index)
    for match in re.finditer(r"\d+(/\d+)?", fps_str):
        try:
            return fractions.Fraction(match.group())
        except ZeroDivisionError:
            continue
    raise MissingInformation(
            f"'ffprobe' did not get a correct framerate in '{filename}' stream {index}"
        )


def get_fps(
    filename: typing.Union[str, bytes, pathlib.Path],
    index: int=0,
    *,
    backend: typing.Union[None, str]=None
) -> numbers.Real:
    """
    ** Reads in the metadata, the average frequency of the frames. **

    Parameters
    ----------
    filename : pathlike
        The pathlike of the file containing a video stream.
    index : int
        The index of the video stream being considered,
        by default the first stream encountered is selected.
    backend : str, optional
        - None (default) : Try to read the stream by trying differents backends.
        - 'ffmpeg' : Uses the modules ``pip install ffmpeg-python``
            which are using the ``ffmpeg`` program in the background.
        - 'cv2' : Uses the module ``pip install opencv-contrib-python-headless``.

    Returns
    -------
    fps : numbers.Real
        The average frequency of the frames in hz.

    Raises
    ------
    MissingStreamError
        If the file does not contain a playable video stream.
    MissingInformation
        If the information is unavailable.
    """
    assert pathlib.Path(filename).exists(), filename
    assert isinstance(index, numbers.Integral), index.__class__.__name__
    assert backend is None or backend in {"ffmpeg", "cv2"}, backend

    filename = str(pathlib.Path(filename))

    if backend == "ffmpeg":
        return _estimate_fps_ffmpeg(filename, index)
    if backend == "cv2":
        return _estimate_fps_cv2(filename, index)

    try:
        return _estimate_fps_ffmpeg(filename, index)
    except (MissingStreamError, MissingInformation):
        return _estimate_fps_cv2(filename, index)
