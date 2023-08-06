#!/usr/bin/env python3

"""
** Allows the pooling of information from several estimation functions. **
--------------------------------------------------------------------------

The function removes the redundancy of the analyses performed by ffmpeg and cv2.
"""

import collections
import numbers
import os
import pathlib
import re
import subprocess
import typing

from movia.core.exceptions import MissingStreamError, MissingInformation


def _check_pathexists_index(filename: typing.Union[str, bytes, pathlib.Path], index: int):
    assert pathlib.Path(filename).exists(), filename
    assert isinstance(index, numbers.Integral), index.__class__.__name__
    assert index >= 0, index

def _decode_duration_frames_ffmpeg(filename: str, index: int) -> tuple[float, int]:
    cmd = [
        "ffmpeg",
        "-threads", "0",
        "-loglevel", "quiet", "-stats",
        "-i", filename,
        "-map", f"0:v:{index}",
        "-c:v", "rawvideo", "-f", "null", os.devnull,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, check=True)
    except subprocess.CalledProcessError as err:
        raise MissingStreamError(f"can not open '{filename}' stream {index} with 'ffmpeg'") from err
    if not (stats := result.stderr.decode()):
        raise MissingInformation(f"'ffmpeg' did not decode '{filename}' stream {index}") from err
    stats = stats.split("\r")[-1].strip()
    if not (duration_match := re.search(r"time=\s*(?P<duration>\d\d:\d\d:\d*\.?\d*)", stats)):
        raise MissingInformation(
            f"'ffmpeg' did not get any time field in '{filename}' stream {index} (out : {stats})"
        ) from err
    hour, minute, second = duration_match["duration"].split(":")
    duration = 3600*float(hour) + 60*float(minute) + float(second)
    if not (nb_match := re.search(r"frame=\s*(?P<nb>[1-9]\d*)", stats)):
        raise MissingInformation(
            f"'ffmpeg' did not get a correct number of frames in '{filename}' stream {index}"
        ) from err
    return duration, int(nb_match["nb"])

def _mix_and_check(
    backend: typing.Union[None, str], accurate: bool, args: tuple, funcs: collections.OrderedDict
) -> typing.Any:

    # checks
    available_backends = {p["backend"] for p in funcs.values()}
    assert backend is None or backend in available_backends, \
        f"{backend} not in {available_backends}"
    assert isinstance(accurate, bool), accurate.__class__.__name__

    # declarations
    def _average(*funcs: typing.Callable) -> typing.Callable:
        return lambda *args: sum(f(*args) for f in funcs) / len(funcs)
    list_funcs = [
        _average(*(f for f, p in funcs.items() if p["accurate"])),
        *funcs
    ]
    err = MissingStreamError("there are no estimators satisfying this request")

    # selection
    if accurate:
        del list_funcs[0]
        for func, prop in funcs.items():
            if not prop["accurate"]:
                list_funcs.remove(func)
    if backend is not None:
        for func, prop in funcs.items():
            if prop["backend"] != backend and func in list_funcs:
                list_funcs.remove(func)

    # execution
    for func in list_funcs:
        try:
            return func(*args)
        except (MissingStreamError, MissingInformation) as err_:
            err = err_
    raise err

def _parse_ffprobe_res(
    cmd: list[str], filename: typing.Union[str, bytes, pathlib.Path], index: int
) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, check=True)
    except subprocess.CalledProcessError as err:
        raise MissingStreamError(f"'ffprobe' can not open '{filename}' stream {index}") from err
    if not (value := result.stdout.decode().strip()):
        raise MissingInformation(f"'ffprobe' did not find any info in '{filename}' stream {index}")
    return value
