#!/usr/bin/env python3

"""
** Recover the date of all the frames that make up a video stream. **
---------------------------------------------------------------------

This information is more accurate than the simple ``fps``
but it takes much longer to retrieve since it requires decoding the entire file.
"""

import numbers
import pathlib
import re
import subprocess
import typing

import cv2 # pip install opencv-contrib-python-headless
import numpy as np

from movia.core.exceptions import MissingStreamError



def _frame_position_cv2(filename: str, index: int) -> np.ndarray:
    """
    ** Retrieve from cv2 the position of the frames in the video. **

    Examples
    --------
    >>> import numpy as np
    >>> from movia.core.analysis.video.properties.timestamps import _interpolate
    >>> from movia.core.analysis.video.properties.timestamps import _frame_position_cv2
    >>> np.round(_interpolate(_frame_position_cv2("movia/examples/video.mp4", 0)), 2)
    array([ 0.  ,  0.04,  0.08,  0.12,  0.16,  0.2 ,  0.24,  0.28,  0.32,
            0.36,  0.4 ,  0.44,  0.48,  0.52,  0.56,  0.6 ,  0.64,  0.68,
            0.72,  0.76,  0.8 ,  0.84,  0.88,  0.92,  0.96,  1.  ,  1.04,
            1.08,  1.12,  1.16,  1.2 ,  1.24,  1.28,  1.32,  1.36,  1.4 ,
            1.44,  1.48,  1.52,  1.56,  1.6 ,  1.64,  1.68,  1.72,  1.76,
            1.8 ,  1.84,  1.88,  1.92,  1.96,  2.  ,  2.04,  2.08,  2.12,
            2.16,  2.2 ,  2.24,  2.28,  2.32,  2.36,  2.4 ,  2.44,  2.48,
            2.52,  2.56,  2.6 ,  2.64,  2.68,  2.72,  2.76,  2.8 ,  2.84,
            2.88,  2.92,  2.96,  3.  ,  3.04,  3.08,  3.12,  3.16,  3.2 ,
            3.24,  3.28,  3.32,  3.36,  3.4 ,  3.44,  3.48,  3.52,  3.56,
            3.6 ,  3.64,  3.68,  3.72,  3.76,  3.8 ,  3.84,  3.88,  3.92,
            3.96,  4.  ,  4.04,  4.08,  4.12,  4.16,  4.2 ,  4.24,  4.28,
            4.32,  4.36,  4.4 ,  4.44,  4.48,  4.52,  4.56,  4.6 ,  4.64,
            4.68,  4.72,  4.76,  4.8 ,  4.84,  4.88,  4.92,  4.96,  5.  ,
            5.04,  5.08,  5.12,  5.16,  5.2 ,  5.24,  5.28,  5.32,  5.36,
            5.4 ,  5.44,  5.48,  5.52,  5.56,  5.6 ,  5.64,  5.68,  5.72,
            5.76,  5.8 ,  5.84,  5.88,  5.92,  5.96,  6.  ,  6.04,  6.08,
            6.12,  6.16,  6.2 ,  6.24,  6.28,  6.32,  6.36,  6.4 ,  6.44,
            6.48,  6.52,  6.56,  6.6 ,  6.64,  6.68,  6.72,  6.76,  6.8 ,
            6.84,  6.88,  6.92,  6.96,  7.  ,  7.04,  7.08,  7.12,  7.16,
            7.2 ,  7.24,  7.28,  7.32,  7.36,  7.4 ,  7.44,  7.48,  7.52,
            7.56,  7.6 ,  7.64,  7.68,  7.72,  7.76,  7.8 ,  7.84,  7.88,
            7.92,  7.96,  8.  ,  8.04,  8.08,  8.12,  8.16,  8.2 ,  8.24,
            8.28,  8.32,  8.36,  8.4 ,  8.44,  8.48,  8.52,  8.56,  8.6 ,
            8.64,  8.68,  8.72,  8.76,  8.8 ,  8.84,  8.88,  8.92,  8.96,
            9.  ,  9.04,  9.08,  9.12,  9.16,  9.2 ,  9.24,  9.28,  9.32,
            9.36,  9.4 ,  9.44,  9.48,  9.52,  9.56,  9.6 ,  9.64,  9.68,
            9.72,  9.76,  9.8 ,  9.84,  9.88,  9.92,  9.96, 10.  , 10.04,
           10.08, 10.12, 10.16, 10.2 , 10.24, 10.28, 10.32, 10.36, 10.4 ,
           10.44, 10.48, 10.52, 10.56, 10.6 , 10.64, 10.68, 10.72, 10.76,
           10.8 , 10.84, 10.88, 10.92, 10.96, 11.  , 11.04, 11.08, 11.12,
           11.16, 11.2 , 11.24, 11.28, 11.32, 11.36, 11.4 , 11.44, 11.48,
           11.52, 11.56, 11.6 , 11.64, 11.68, 11.72, 11.76, 11.8 , 11.84,
           11.88, 11.92, 11.96, 12.  , 12.04, 12.08, 12.12, 12.16, 12.2 ,
           12.24, 12.28, 12.32, 12.36, 12.4 , 12.44, 12.48, 12.52, 12.56,
           12.6 , 12.64, 12.68, 12.72, 12.76, 12.8 , 12.84, 12.88, 12.92,
           12.96, 13.  , 13.04, 13.08, 13.12, 13.16, 13.2 , 13.24, 13.28,
           13.32, 13.36, 13.4 , 13.44, 13.48, 13.52, 13.56, 13.6 , 13.64,
           13.68, 13.72, 13.76, 13.8 , 13.84, 13.88, 13.92, 13.96, 14.  ,
           14.04, 14.08, 14.12, 14.16, 14.2 , 14.24, 14.28, 14.32, 14.36,
           14.4 , 14.44, 14.48, 14.52, 14.56, 14.6 , 14.64, 14.68, 14.72,
           14.76, 14.8 , 14.84, 14.88, 14.92, 14.96, 15.  , 15.04, 15.08,
           15.12, 15.16, 15.2 , 15.24, 15.28, 15.32, 15.36, 15.4 , 15.44,
           15.48, 15.52, 15.56, 15.6 , 15.64, 15.68, 15.72, 15.76, 15.8 ,
           15.84, 15.88, 15.92, 15.96], dtype=float32)
    >>>
    """
    cap = cv2.VideoCapture(filename, index)
    if not cap.isOpened():
        raise MissingStreamError(f"impossible to open '{filename}' stream {index} with 'cv2'")

    pos_list = []

    while True:
        if not cap.read()[0]:
            break
        pos_curr = cap.get(cv2.CAP_PROP_POS_MSEC)
        if pos_curr == 0.0 and pos_list:
            pos_list.append(np.nan)
        else:
            pos_list.append(pos_curr)
    cap.release()

    if not pos_list:
        raise MissingStreamError(f"'cv2' does not detect any frame in '{filename}' stream {index}")
    if np.all(np.isnan(pos_list)):
        raise MissingStreamError(
            f"'cv2' is unable to locate the frames of '{filename}' stream {index}"
        )

    return 1e-3 * np.array(pos_list, dtype=np.float32)


def _frame_position_ffmpeg(filename: str, index: int) -> np.ndarray:
    """
    ** Retrieve from ffmpeg the position of the frames in the video. **

    Examples
    --------
    >>> import numpy as np
    >>> from movia.core.analysis.video.properties.timestamps import _interpolate
    >>> from movia.core.analysis.video.properties.timestamps import _frame_position_ffmpeg
    >>> np.round(_interpolate(_frame_position_ffmpeg("movia/examples/video.mp4", 0)), 2)
    array([ 0.  ,  0.04,  0.08,  0.12,  0.16,  0.2 ,  0.24,  0.28,  0.32,
            0.36,  0.4 ,  0.44,  0.48,  0.52,  0.56,  0.6 ,  0.64,  0.68,
            0.72,  0.76,  0.8 ,  0.84,  0.88,  0.92,  0.96,  1.  ,  1.04,
            1.08,  1.12,  1.16,  1.2 ,  1.24,  1.28,  1.32,  1.36,  1.4 ,
            1.44,  1.48,  1.52,  1.56,  1.6 ,  1.64,  1.68,  1.72,  1.76,
            1.8 ,  1.84,  1.88,  1.92,  1.96,  2.  ,  2.04,  2.08,  2.12,
            2.16,  2.2 ,  2.24,  2.28,  2.32,  2.36,  2.4 ,  2.44,  2.48,
            2.52,  2.56,  2.6 ,  2.64,  2.68,  2.72,  2.76,  2.8 ,  2.84,
            2.88,  2.92,  2.96,  3.  ,  3.04,  3.08,  3.12,  3.16,  3.2 ,
            3.24,  3.28,  3.32,  3.36,  3.4 ,  3.44,  3.48,  3.52,  3.56,
            3.6 ,  3.64,  3.68,  3.72,  3.76,  3.8 ,  3.84,  3.88,  3.92,
            3.96,  4.  ,  4.04,  4.08,  4.12,  4.16,  4.2 ,  4.24,  4.28,
            4.32,  4.36,  4.4 ,  4.44,  4.48,  4.52,  4.56,  4.6 ,  4.64,
            4.68,  4.72,  4.76,  4.8 ,  4.84,  4.88,  4.92,  4.96,  5.  ,
            5.04,  5.08,  5.12,  5.16,  5.2 ,  5.24,  5.28,  5.32,  5.36,
            5.4 ,  5.44,  5.48,  5.52,  5.56,  5.6 ,  5.64,  5.68,  5.72,
            5.76,  5.8 ,  5.84,  5.88,  5.92,  5.96,  6.  ,  6.04,  6.08,
            6.12,  6.16,  6.2 ,  6.24,  6.28,  6.32,  6.36,  6.4 ,  6.44,
            6.48,  6.52,  6.56,  6.6 ,  6.64,  6.68,  6.72,  6.76,  6.8 ,
            6.84,  6.88,  6.92,  6.96,  7.  ,  7.04,  7.08,  7.12,  7.16,
            7.2 ,  7.24,  7.28,  7.32,  7.36,  7.4 ,  7.44,  7.48,  7.52,
            7.56,  7.6 ,  7.64,  7.68,  7.72,  7.76,  7.8 ,  7.84,  7.88,
            7.92,  7.96,  8.  ,  8.04,  8.08,  8.12,  8.16,  8.2 ,  8.24,
            8.28,  8.32,  8.36,  8.4 ,  8.44,  8.48,  8.52,  8.56,  8.6 ,
            8.64,  8.68,  8.72,  8.76,  8.8 ,  8.84,  8.88,  8.92,  8.96,
            9.  ,  9.04,  9.08,  9.12,  9.16,  9.2 ,  9.24,  9.28,  9.32,
            9.36,  9.4 ,  9.44,  9.48,  9.52,  9.56,  9.6 ,  9.64,  9.68,
            9.72,  9.76,  9.8 ,  9.84,  9.88,  9.92,  9.96, 10.  , 10.04,
           10.08, 10.12, 10.16, 10.2 , 10.24, 10.28, 10.32, 10.36, 10.4 ,
           10.44, 10.48, 10.52, 10.56, 10.6 , 10.64, 10.68, 10.72, 10.76,
           10.8 , 10.84, 10.88, 10.92, 10.96, 11.  , 11.04, 11.08, 11.12,
           11.16, 11.2 , 11.24, 11.28, 11.32, 11.36, 11.4 , 11.44, 11.48,
           11.52, 11.56, 11.6 , 11.64, 11.68, 11.72, 11.76, 11.8 , 11.84,
           11.88, 11.92, 11.96, 12.  , 12.04, 12.08, 12.12, 12.16, 12.2 ,
           12.24, 12.28, 12.32, 12.36, 12.4 , 12.44, 12.48, 12.52, 12.56,
           12.6 , 12.64, 12.68, 12.72, 12.76, 12.8 , 12.84, 12.88, 12.92,
           12.96, 13.  , 13.04, 13.08, 13.12, 13.16, 13.2 , 13.24, 13.28,
           13.32, 13.36, 13.4 , 13.44, 13.48, 13.52, 13.56, 13.6 , 13.64,
           13.68, 13.72, 13.76, 13.8 , 13.84, 13.88, 13.92, 13.96, 14.  ,
           14.04, 14.08, 14.12, 14.16, 14.2 , 14.24, 14.28, 14.32, 14.36,
           14.4 , 14.44, 14.48, 14.52, 14.56, 14.6 , 14.64, 14.68, 14.72,
           14.76, 14.8 , 14.84, 14.88, 14.92, 14.96, 15.  , 15.04, 15.08,
           15.12, 15.16, 15.2 , 15.24, 15.28, 15.32, 15.36, 15.4 , 15.44,
           15.48, 15.52, 15.56, 15.6 , 15.64, 15.68, 15.72, 15.76, 15.8 ,
           15.84, 15.88, 15.92, 15.96], dtype=float32)
    >>>
    """
    cmd = [
        "ffprobe",
        "-threads", "0",
        "-v", "error",
        "-show_frames",
        "-count_frames",
        "-select_streams", f"v:{index}",
        "-show_entries",
        "frame=pts_time,pkt_dts_time,best_effort_timestamp_time:stream=nb_read_frames",
        "-of", "default=nokey=0:noprint_wrappers=1",
        filename,
    ]
    try: # sudo apt install ffmpeg
        result = subprocess.run(cmd, capture_output=True, check=True)
    except subprocess.CalledProcessError as err:
        raise MissingStreamError(f"can not open '{filename}' stream {index} with 'ffmpeg'") from err
    if not (result_str := result.stdout.decode()):
        raise MissingStreamError(f"'ffprobe' did not find any frames '{filename}' stream {index}")

    # get nb frames
    if (_nb_frames := re.search(r"nb_read_frames\s*=\s*(?P<nb_frames>[0-9]+)", result_str)) is None:
        raise MissingStreamError(
            f"'ffprobe' cannot find the number of frames in '{filename}' stream {index}"
        )
    if not (nb_frames := int(_nb_frames["nb_frames"])):
        raise MissingStreamError(
            f"'ffprobe' pretends that there are 0 frames in '{filename}' stream {index}"
        )

    # get positions
    pts_list = np.array([
        np.nan if line[9:] == "N/A" else float(line[9:])
        for line in result_str.split("\n")
        if line.startswith("pts_time") # display time
    ], dtype=np.float32) # only for ffmpeg >= 5, empty list for ffmpeg4
    dts_list = np.array([
        np.nan if line[13:] == "N/A" else float(line[13:])
        for line in result_str.split("\n")
        if line.startswith("pkt_dts_time") # decode time
    ], dtype=np.float32)
    best_list = np.array([
        np.nan if line[27:] == "N/A" else float(line[27:])
        for line in result_str.split("\n")
        if line.startswith("best_effort_timestamp_time") # display time
    ], dtype=np.float32)
    assert len(pts_list) in {0, nb_frames} # for ffmpeg4
    assert len(dts_list) == nb_frames
    assert len(dts_list) == nb_frames

    if len(pts_list) == 0: # for ffmpeg4
        pos_list = dts_list
    else:
        pos_list = np.where(np.isnan(pts_list), dts_list, pts_list)
    pos_list = np.where(np.isnan(pos_list), best_list, pos_list)

    if np.all(np.isnan(pos_list)):
        raise MissingStreamError(
            f"'ffprobe' is unable to locate the frames of '{filename}' stream {index}"
        )
    return pos_list


def _interpolate(sequence: np.ndarray) -> np.ndarray:
    """
    ** Interpolates a numpy vector to replace the nan with a consistent value. **

    The interpolation is a linear interpolation based on the least squares.

    Parameters
    ----------
    sequence : np.ndarray
        The 1d vector containing nan.

    Returns
    -------
    interp : np.ndarray
        The input vector with the nan replaced by their interpolated value.

    Notes
    -----
    Modifies directly the values of the array, does not make a copy.

    Examples
    --------
    >>> import numpy as np
    >>> from movia.core.analysis.video.properties.timestamps import _interpolate
    >>> a = lambda l: np.array(l, dtype=np.float32)
    >>> r = lambda v: np.round(v, 5)
    >>> r(_interpolate(a([0.0, np.nan, 1.0])))
    array([0. , 0.5, 1. ], dtype=float32)
    >>> r(_interpolate(a([np.nan, 0.5, 1.0])))
    array([0. , 0.5, 1. ], dtype=float32)
    >>> r(_interpolate(a([0.0, 0.5, np.nan])))
    array([0. , 0.5, 1. ], dtype=float32)
    >>>
    """
    assert isinstance(sequence, np.ndarray)
    assert sequence.ndim == 1

    nans = np.isnan(sequence)
    not_nans = ~nans
    grade, mean = np.polyfit(np.arange(len(sequence))[not_nans], sequence[not_nans], deg=1)

    sequence[nans] = mean + grade*np.arange(len(sequence))[nans]
    return sequence


def get_frames_timestamp(
    filename: typing.Union[str, bytes, pathlib.Path],
    index: int=0,
    *,
    backend: typing.Union[None, str]=None,
    interpolate: bool=True
) -> np.ndarray:
    """
    ** Recover the date of appearance of the frames. **

    In case the frame rate is perfectly constant, this returns
    ``[0, 1/fps, 2/fps, ..., (n-1)/fps]`` with n the number of frames present in the video.
    But in case the frequency of images is not quite constant, this function has more interest.

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
    interpolate : bool, optional
        If True (default), then the frames whose position is unknown
        are interpolated from the set of correctly dated frames.
        If False, the unconfirmed positions are translated as 'np.nan'.

    Returns
    -------
    dates : np.ndarray
        The numpy 1d list containing the dates in seconds, encoded in float32.

    Raises
    ------
    MissingStreamError
        If the file does not contain a playable video stream.
    """
    assert pathlib.Path(filename).exists(), filename
    assert isinstance(index, numbers.Integral), index.__class__.__name__
    assert backend is None or backend in {"ffmpeg", "cv2"}, backend
    assert isinstance(interpolate, bool), interpolate.__class__.__name__

    def inter(sequence):
        if not interpolate or not np.any(np.isnan(sequence)):
            return sequence
        return _interpolate(sequence)

    filename = str(pathlib.Path(filename))

    if backend == "ffmpeg":
        return inter(_frame_position_ffmpeg(filename, index))
    if backend == "cv2":
        return inter(_frame_position_cv2(filename, index))

    try:
        return inter(_frame_position_cv2(filename, index))
    except (MissingStreamError, ImportError):
        return inter(_frame_position_ffmpeg(filename, index))
