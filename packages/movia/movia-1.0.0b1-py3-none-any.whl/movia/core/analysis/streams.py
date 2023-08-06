#!/usr/bin/env python3

"""
** Detects the different streams of a multimedia file. **
---------------------------------------------------------
"""


import pathlib
import subprocess
import typing

from movia.core.exceptions import MissingStreamError



def get_streams_type(
    filename: typing.Union[str, bytes, pathlib.Path], ignore_errors=False
) -> list[str]:
    """
    ** Retrieves in order the stream types present in the file. **

    Parameters
    ----------
    filename : pathlike
        The pathlike of the file containing streams.
    ignore_errors : boolean, default=False
        If True, returns an empty list
        rather than throwing an exception if no valid stream is detected.


    Returns
    -------
    streams_type : list[str]
        Each item can be "audio", "subtitle" or "video".

    Raises
    ------
    MissingStreamError
        If ``ignore_errors`` is False and if one of the indexes is missing or redondant.

    Examples
    --------
    >>> from movia.core.analysis.streams import get_streams_type
    >>> get_streams_type("movia/examples/intro.mkv")
    ['video', 'video', 'audio', 'audio']
    >>> get_streams_type("movia/examples/project.pk", ignore_errors=True)
    []
    >>>
    """
    filename = pathlib.Path(filename)
    assert filename.exists(), filename
    filename = str(filename)
    assert isinstance(ignore_errors, bool), ignore_errors.__class__.__name__

    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "stream=index,codec_type",
        "-of", "csv=p=0",
        filename,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, check=True)
    except subprocess.CalledProcessError as err:
        if ignore_errors:
            return []
        raise MissingStreamError(f"'ffprobe' can not open '{filename}'") from err
    if not (indexs_streams := result.stdout.decode().strip().split("\n")):
        if ignore_errors:
            return []
        raise MissingStreamError(f"'ffprobe' did not find any stream info in '{filename}'")

    indexs_streams = list(filter(lambda index_stream: bool(index_stream), indexs_streams))
    streams = [None for _ in range(len(indexs_streams))]
    for index_stream in indexs_streams:
        index, stream, *_ = index_stream.split(",")
        index = int(index)
        if index < 0 or index >= len(streams):
            if ignore_errors:
                return []
            raise MissingStreamError(f"missing stream index in '{filename}', {indexs_streams}")
        if streams[index] is not None:
            if ignore_errors:
                return []
            raise MissingStreamError(f"index {index} appears twice in '{filename}'")
        if stream not in {"audio", "subtitle", "video"}:
            raise ValueError(
                f"the stream {index} ({stream}) in '{filename}' "
                "not in 'audio', 'video' or 'subtitle'"
            )
        streams[index] = stream

    return streams
