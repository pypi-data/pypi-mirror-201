#!/usr/bin/env python3


"""
** Allows to generate a multitude of objects. **
------------------------------------------------

Doesn't perform any test itself but allows to lighten the other tests.
"""

import math

import typing

from movia.core.classes.container import ContainerOutput
from movia.core.classes.node import Node
from movia.core.filters.basic.translate import FilterTranslate
from movia.core.filters.basic.truncate import FilterTruncate
from movia.core.generation.audio.empty import GeneratorAudioEmpty
from movia.core.generation.audio.noise import GeneratorAudioNoise
from movia.core.generation.video.empty import GeneratorVideoEmpty
from movia.core.generation.video.equation import GeneratorVideoEquation
from movia.core.generation.video.noise import GeneratorVideoNoise
from movia.core.io.read import ContainerInputFFMPEG
from movia.core.io.write import ContainerOutputFFMPEG



OBJECTS = {} # to each class, associates the list of generated instances



def add_generator(func: typing.Callable):
    """
    ** Simplifies the future management of the different generators. **

    Automatically generate streams from nodes.
    """
    for obj in func():
        OBJECTS[obj.__class__] = OBJECTS.get(obj.__class__, [])
        OBJECTS[obj.__class__].append(obj)
        if isinstance(obj, Node):
            for stream in obj.out_streams:
                OBJECTS[stream.__class__] = OBJECTS.get(stream.__class__, [])
                OBJECTS[stream.__class__].append(stream)
    return func


@add_generator
def generate_container_input_ffmpeg():
    """
    ** Generates several ``movia.core.io.read.ContainerInputFFMPEG``. **
    """
    yield ContainerInputFFMPEG("movia/examples/video.mp4")
    yield ContainerInputFFMPEG("movia/examples/audio.ogg")
    yield ContainerInputFFMPEG("movia/examples/intro.mkv")
    yield ContainerInputFFMPEG("movia/examples/video.mp4", buffer_size=16384)


@add_generator
def generate_container_output():
    """
    ** Generates several ``movia.core.classes.container.ContainerOutput``. **
    """
    yield ContainerOutput(ContainerInputFFMPEG("movia/examples/video.mp4").out_streams)
    yield ContainerOutput(ContainerInputFFMPEG("movia/examples/audio.ogg").out_streams)
    yield ContainerOutput(ContainerInputFFMPEG("movia/examples/intro.mkv").out_streams)


@add_generator
def generate_container_output_ffmpeg():
    """
    ** Generates several ``movia.core.io.read.ContainerOutputFFMPEG``. **
    """
    audio_set = [{"codec": "mp3", "rate": 44100}, {"codec": "aac", "rate": 16000}]
    video_set = [{"codec": "h264", "rate": 24}, {"codec": "h264", "rate": 12}]
    yield ContainerOutputFFMPEG(
        ContainerInputFFMPEG("movia/examples/video.mp4").out_streams,
        "filename",
        streams_settings=[video_set[0]],
    )
    yield ContainerOutputFFMPEG(
        ContainerInputFFMPEG("movia/examples/audio.ogg").out_streams,
        "filename",
        streams_settings=[audio_set[0]],
    )
    yield ContainerOutputFFMPEG(
        [
            ContainerInputFFMPEG("movia/examples/video.mp4").out_streams[0],
            ContainerInputFFMPEG("movia/examples/audio.ogg").out_streams[0],
        ],
        "filename",
        streams_settings=[video_set[0], audio_set[0]],
    )
    yield ContainerOutputFFMPEG(
        ContainerInputFFMPEG("movia/examples/video.mp4").out_streams,
        "filename_bis",
        streams_settings=[video_set[0]],
    )
    yield ContainerOutputFFMPEG(
        ContainerInputFFMPEG("movia/examples/video.mp4").out_streams,
        "filename",
        streams_settings=[video_set[1]],
    )


@add_generator
def generate_filter_translate():
    """
    ** Generates several ``movia.core.filters.basic.translate.FilterTranslate``. **
    """
    for container in (
        ContainerInputFFMPEG("movia/examples/video.mp4"),
        ContainerInputFFMPEG("movia/examples/audio.ogg"),
        GeneratorAudioNoise.default(),
        GeneratorVideoNoise.default(),
    ):
        yield FilterTranslate(container.out_streams, 0)
        yield FilterTranslate(container.out_streams, 1)


@add_generator
def generate_filter_truncate():
    """
    ** Generates several ``movia.core.filters.basic.truncate.FilterTruncate``. **
    """
    for container in (
        ContainerInputFFMPEG("movia/examples/video.mp4"),
        ContainerInputFFMPEG("movia/examples/audio.ogg"),
        GeneratorAudioNoise.default(),
        GeneratorVideoNoise.default(),
    ):
        ref_duration = min(s.duration for s in container.out_streams)
        for duration in sorted({0, max(0, ref_duration-1), ref_duration, ref_duration+1, math.inf}):
            yield FilterTruncate(container.out_streams, duration)


@add_generator
def generate_generator_audio_empty():
    """
    ** Generates several ``movia.core.generation.audio.empty.GeneratorAudioEmpty``. **
    """
    yield GeneratorAudioEmpty()


@add_generator
def generate_generator_audio_noise():
    """
    ** Generates several ``movia.core.generation.audio.noise.GeneratorAudioNoise``. **
    """
    yield GeneratorAudioNoise(0) # fixed
    yield GeneratorAudioNoise() # random init


@add_generator
def generate_generator_video_empty():
    """
    ** Generates several ``movia.core.generation.audio.empty.GeneratorAudioEmpty``. **
    """
    yield GeneratorVideoEmpty()


@add_generator
def generate_generator_video_equation():
    """
    ** Generates several ``movia.core.generation.video.equation.GeneratorVideoEquation``. **
    """
    yield GeneratorVideoEquation("0", "0", "0") # black video
    yield GeneratorVideoEquation("1", "1", "1") # white video
    yield GeneratorVideoEquation("1", "0", "0") # blue video
    yield GeneratorVideoEquation("0", "1", "0") # green video
    yield GeneratorVideoEquation("0", "0", "1") # red video
    yield GeneratorVideoEquation("t", "t", "t") # simple t depending
    yield GeneratorVideoEquation("1/2 + 1/2*i", "1/2 + 1/2*i", "1/2 + 1/2*i") # simple i depending
    yield GeneratorVideoEquation("1/2 + 1/2*j", "1/2 + 1/2*j", "1/2 + 1/2*j") # simple j depending
    yield GeneratorVideoEquation(
        "atan(pi*j)/pi + 1/2", # dark blue on the left and bright on the right
        "sin(2pi(i-t))**2", # horizontal descending green waves
        "exp(-(i**2+j**2)/(2*(1e-3+.1*t)))", # red spot in the center that grows
    ) # complexe expression


@add_generator
def generate_generator_video_noise():
    """
    ** Generates several ``movia.core.generation.video.noise.GeneratorVideoNoise``. **
    """
    yield GeneratorVideoNoise(0) # fixed
    yield GeneratorVideoNoise() # random init
