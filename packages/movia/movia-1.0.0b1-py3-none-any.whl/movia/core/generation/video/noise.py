#!/usr/bin/env python3

"""
** Generate a video noise signal. **
------------------------------------
"""

import numbers
import random
import struct
import typing

import torch

from movia.core.classes.container import ContainerInput
from movia.core.classes.frame_video import FrameVideo
from movia.core.classes.stream import Stream
from movia.core.classes.stream_video import StreamVideo



class GeneratorVideoNoise(ContainerInput):
    """
    ** Generate a pure noise video signal. **

    Attributes
    ----------
    seed : float
        The value of the seed between 0 and 1 (readonly).
    shape : tuple[int, int]
        The vertical and horizontal (i, j) resolution of the image (readonly).

    Examples
    --------
    >>> from movia.core.generation.video.noise import GeneratorVideoNoise
    >>> stream = GeneratorVideoNoise(0, shape=(13, 9)).out_streams[0]
    >>> stream.snapshot(0)[..., 0]
    FrameVideo([[172, 192, 195, 211,  36, 216,  58,  39,  88],
                [ 25,   9, 208, 254, 192, 216,  29, 142, 193],
                [127, 202, 163, 114,  34, 164,  38,  17, 105],
                [ 31,  65,  57, 119,  82, 142, 140,  84,   6],
                [127, 204, 232, 148,  23, 117,  49, 163, 197],
                [113, 162, 131, 205, 149,   0,  43,  23, 121],
                [163, 195, 227,  50,  41,  36,  43,   2,  32],
                [ 38,  42, 188,  30,   2, 226, 112,  19, 154],
                [180,  61,   4, 139, 205,  75, 152, 110, 188],
                [117, 161, 228, 121,  31, 184,  41, 182, 166],
                [249, 118, 125, 210, 234,  35, 189,  43, 104],
                [182, 125, 232, 211,  53, 148,  67, 137, 151],
                [218,   3, 138, 199,  85,  34,  33, 255, 203]], dtype=torch.uint8, metadata=0.0)
    >>>
    """

    def __init__(
        self,
        seed: numbers.Real = None,
        shape: typing.Union[tuple[numbers.Integral, numbers.Integral], list[numbers.Integral]] = (
            720,
            720,
        ),
    ):
        """
        Parameters
        ----------
        seed : numbers.Real
            The random seed to have a repeatability.
            The value must be between 0 included and 1 excluded.
            If not provided, the seed is chosen randomly.
        shape : tuple or list, optional
            The pixel dimensions of the generated frames.
            The convention adopted is the numpy convention (height, width)
        """
        # check
        if seed is None:
            seed = random.random()
        assert isinstance(seed, numbers.Real), seed.__class__.__name__
        assert 0 <= seed < 1, seed
        assert isinstance(shape, (tuple, list)), shape.__class__.__name__
        assert len(shape) == 2, shape
        assert all(isinstance(s, numbers.Integral) and s > 0 for s in shape)

        # declaration
        self._seed = float(seed)
        self._height, self._width = int(shape[0]), int(shape[1])

        # delegation
        super().__init__([_StreamVideoNoiseUniform(self)])

    @classmethod
    def default(cls):
        return cls(0)

    def getstate(self) -> dict:
        return {
            "seed": self.seed,
            "shape": self.shape,
        }

    @property
    def seed(self):
        """
        ** The value of the seed between 0 and 1. **
        """
        return self._seed

    def setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        keys = {"seed", "shape"}
        assert set(state) == keys, set(state) - keys
        GeneratorVideoNoise.__init__(self, seed=state["seed"], shape=state["shape"])

    @property
    def shape(self) -> list[int, int]:
        """
        ** The vertical and horizontal (i, j) resolution of the image. **
        """
        return [self._height, self._width]


class _StreamVideoNoiseUniform(StreamVideo):
    """
    ** Random video stream where each pixel follows a uniform law. **
    """

    is_space_continuous = True
    is_time_continuous = True

    def __init__(self, node: GeneratorVideoNoise):
        assert isinstance(node, GeneratorVideoNoise), node.__class__.__name__
        super().__init__(node)

    def _snapshot(self, timestamp: float) -> FrameVideo:
        return FrameVideo(
            timestamp,
            torch.randint(
                0,
                256,
                (self.height, self.width, 3),
                generator=torch.random.manual_seed(
                    int.from_bytes(struct.pack("dd", self.node.seed, timestamp), byteorder="big")
                    % (1 << 64) # solve RuntimeError: Overflow when unpacking long
                ),
                dtype=torch.uint8
            ),
        )
