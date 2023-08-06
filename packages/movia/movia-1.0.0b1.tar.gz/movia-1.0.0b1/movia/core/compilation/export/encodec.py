#!/usr/bin/env python3

"""
** Allows to suggest an appropriate encoder. **
-----------------------------------------------
"""


def suggest_encodec(type_: str):
    """
    ** Returns the name of an ffmpeg container format appropriate for the given parameters. **

    Parameters
    ----------
    type_ : str
        The type of stream, "audio", "video" or "subtitle".
    """
    assert isinstance(type_, str), type_.__class__.__name__
    assert type_ in {"audio", "subtitle", "video"}, type_

    if type_ == "audio":
        return "libopus"
    if type_ == "video":
        return "libaom-av1"
    raise TypeError(f"not yet supported {type_}")
