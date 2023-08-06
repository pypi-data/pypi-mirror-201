#!/usr/bin/env python3

"""
** Find the default settings for ``movia.core.io.write.ContainerOutputFFMPEG``. **
----------------------------------------------------------------------------------
"""

import pathlib
import typing

from movia.core.classes.stream import Stream
from movia.core.compilation.export.compatibility import MuxerInfos
from movia.core.compilation.export.encodec import suggest_encodec
from movia.core.compilation.export.muxer import suggest_muxer
from movia.core.compilation.export.rate_audio import find_optimal_audio_rate
from movia.core.compilation.export.rate_video import find_optimal_video_rate


def suggest_export_params(
    in_streams: typing.Iterable[Stream],
    *,
    filename: typing.Union[str, bytes, pathlib.Path]="movia_project",
    muxer: str="default",
    encodecs: typing.Iterable[str]=None,
):
    """
    ** Suggests a combination of suitable parameters. **

    Parameters
    ----------
    in_streams : typing.Iterable[Stream]
        The streams to be encoded.
    filename : pathlike, optional
        The final file, relative or absolute.
        If the suffix is provided, it allows to find the muxer (if it is not already provided).
        If the muxer is provided, the associated suffix is added to the file name
        (if the filename has no suffix)
    muxer : str, optional
        The name of the muxer ffmpeg, it is call "format" in pyav and in returs parameters.
        The special value "default" means that this function will decide.
    encodecs : list[str], optional
        For each stream, corresponds to the name of the associated codec or encoder.
        The special value "default" means that this function will decide.

    Returns
    -------
    filename : pathlib.Path
        A default file name with the appropriate suffix.
    streams_settings : list[dict]
        Information related to each codec. Items are:
            * "codec": str, # the encoder name
            * "rate": str, # the number of elements per second
    container_settings : dict
        Global container file information. Items are:
            * "format": str or None, # specific format / muxer to use
            * "options": dict, # options to pass to the container and all streams
            * "container_options": dict, # options to pass to the container
    """
    assert hasattr(in_streams, "__iter__"), in_streams.__class__.__name__
    in_streams = tuple(in_streams)
    assert all(isinstance(s, Stream) for s in in_streams), in_streams
    assert isinstance(filename, (str, bytes, pathlib.Path)), filename.__class__.__name__
    filename = pathlib.Path(filename)
    assert isinstance(muxer, str), muxer.__class__.__name__
    muxer = str(muxer)
    if encodecs is None:
        encodecs = ["default" for _ in in_streams]
    else:
        assert hasattr(encodecs, "__iter__"), encodecs.__class__.__name__
        encodecs = list(encodecs)
        assert len(encodecs) == len(in_streams), (encodecs, in_streams)
        assert all(isinstance(e, str) for e in encodecs), encodecs

    # find muxer if no suffix and no muxer provide
    if not filename.suffix and muxer == "default":
        muxer = suggest_muxer()

    # add suffix if muxer is given
    if not filename.suffix and muxer != "default":
        if (extensions := MuxerInfos(muxer).extensions):
            filename = filename.with_suffix(sorted(extensions)[0])

    # find muxer if suffix is given
    if filename.suffix and muxer == "default":
        muxer = MuxerInfos.from_suffix(filename.suffix)

    # find encodec if not provide
    for i, (stream, encodec) in enumerate(zip(in_streams, encodecs.copy())):
        if encodec == "default":
            encodecs[i] = suggest_encodec(stream.type)

    # parse
    streams_settings = []
    for stream, encodec in zip(in_streams, encodecs.copy()):
        if stream.type == "audio":
            streams_settings.append({"codec": encodec, "rate": find_optimal_audio_rate(stream)})
        elif stream.type == "video":
            streams_settings.append(
                {"codec": encodec, "rate": str(find_optimal_video_rate(stream))}
            )
        else:
            raise TypeError(f"not yet supported {stream.type}")
    container_settings = {"format": "matroska", "options": {}, "container_options": {}}
    return filename, streams_settings, container_settings
