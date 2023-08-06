#!/usr/bin/env python3

"""
** Allows to generate colors from continuous mathematical functions. **
-----------------------------------------------------------------------
"""


import numbers
import tokenize
import typing
import warnings

from sympy.core import sympify, Expr, oo, Symbol
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication
from sympy.utilities.lambdify import lambdify
import numpy as np
import torch

from movia.core.classes.container import ContainerInput
from movia.core.classes.frame_video import FrameVideo
from movia.core.classes.stream import Stream
from movia.core.classes.stream_video import StreamVideo



SYMBOLS = {
    "t": Symbol("t", real=True, positive=True),
    "i": Symbol("i", real=True),
    "j": Symbol("j", real=True),
    "oo": oo
}



class GeneratorVideoEquation(ContainerInput):
    """
    ** Generate a video stream whose channels are defened by any equations. **

    Attributes
    ----------
    b_expr : sympy.core.expr.Expr
        The luminosity expression for the blue channel (readonly).
    g_expr : sympy.core.expr.Expr
        The luminosity expression for the green channel (readonly).
    r_expr : sympy.core.expr.Expr
        The luminosity expression for the red channel (readonly).
    shape : tuple[int, int]
        The vertical and horizontal (i, j) resolution of the image (readonly).

    Examples
    --------
    >>> from movia.core.generation.video.equation import GeneratorVideoEquation
    >>> (stream,) = GeneratorVideoEquation(
    ...     "atan(pi*j)/pi + 1/2", # dark blue on the left and bright on the right
    ...     "sin(2pi(i-t))**2", # horizontal descending green waves
    ...     "exp(-(i**2+j**2)/(2*(1e-3+.1*t)))", # red spot in the center that grows
    ...     shape=(13, 9),
    ... ).out_streams
    >>> stream.node.b_expr
    atan(pi*j)/pi + 1/2
    >>> stream.node.g_expr
    sin(pi*(2*i - 2*t))**2
    >>> stream.node.r_expr
    exp((-i**2 - j**2)/(0.2*t + 0.002))
    >>> stream.snapshot(0)[..., 0] # blue at t=0
    FrameVideo([[ 25,  33,  46,  73, 128, 182, 209, 222, 230],
                [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
                [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
                [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
                [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
                [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
                [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
                [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
                [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
                [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
                [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
                [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
                [ 25,  33,  46,  73, 128, 182, 209, 222, 230]], dtype=torch.uint8, metadata=0.0)
    >>> stream.snapshot(0)[..., 1] # green at t=0
    FrameVideo([[  0,   0,   0,   0,   0,   0,   0,   0,   0],
                [191, 191, 191, 191, 191, 191, 191, 191, 191],
                [191, 191, 191, 191, 191, 191, 191, 191, 191],
                [  0,   0,   0,   0,   0,   0,   0,   0,   0],
                [191, 191, 191, 191, 191, 191, 191, 191, 191],
                [191, 191, 191, 191, 191, 191, 191, 191, 191],
                [  0,   0,   0,   0,   0,   0,   0,   0,   0],
                [191, 191, 191, 191, 191, 191, 191, 191, 191],
                [191, 191, 191, 191, 191, 191, 191, 191, 191],
                [  0,   0,   0,   0,   0,   0,   0,   0,   0],
                [191, 191, 191, 191, 191, 191, 191, 191, 191],
                [191, 191, 191, 191, 191, 191, 191, 191, 191],
                [  0,   0,   0,   0,   0,   0,   0,   0,   0]], dtype=torch.uint8, metadata=0.0)
    >>> stream.snapshot(0)[..., 2] # red at t=0
    FrameVideo([[  0,   0,   0,   0,   0,   0,   0,   0,   0],
                [  0,   0,   0,   0,   0,   0,   0,   0,   0],
                [  0,   0,   0,   0,   0,   0,   0,   0,   0],
                [  0,   0,   0,   0,   0,   0,   0,   0,   0],
                [  0,   0,   0,   0,   0,   0,   0,   0,   0],
                [  0,   0,   0,   0,   0,   0,   0,   0,   0],
                [  0,   0,   0,   0, 255,   0,   0,   0,   0],
                [  0,   0,   0,   0,   0,   0,   0,   0,   0],
                [  0,   0,   0,   0,   0,   0,   0,   0,   0],
                [  0,   0,   0,   0,   0,   0,   0,   0,   0],
                [  0,   0,   0,   0,   0,   0,   0,   0,   0],
                [  0,   0,   0,   0,   0,   0,   0,   0,   0],
                [  0,   0,   0,   0,   0,   0,   0,   0,   0]], dtype=torch.uint8, metadata=0.0)
    >>> stream.snapshot(1)[..., 2] # red at t=1
    FrameVideo([[  0,   0,   1,   1,   2,   1,   1,   0,   0],
                [  0,   1,   2,   6,   8,   6,   2,   1,   0],
                [  0,   2,   8,  21,  28,  21,   8,   2,   0],
                [  1,   5,  21,  54,  74,  54,  21,   5,   1],
                [  1,   9,  43, 108, 147, 108,  43,   9,   1],
                [  2,  14,  64, 163, 222, 163,  64,  14,   2],
                [  2,  16,  74, 187, 255, 187,  74,  16,   2],
                [  2,  14,  64, 163, 222, 163,  64,  14,   2],
                [  1,   9,  43, 108, 147, 108,  43,   9,   1],
                [  1,   5,  21,  54,  74,  54,  21,   5,   1],
                [  0,   2,   8,  21,  28,  21,   8,   2,   0],
                [  0,   1,   2,   6,   8,   6,   2,   1,   0],
                [  0,   0,   1,   1,   2,   1,   1,   0,   0]], dtype=torch.uint8, metadata=1.0)
    >>>
    """

    def __init__(self,
        b_expr: typing.Union[str, Expr],
        g_expr: typing.Union[str, Expr],
        r_expr: typing.Union[str, Expr],
        shape: typing.Union[tuple[numbers.Integral, numbers.Integral], list[numbers.Integral]] = (
            720,
            720,
        ),
    ):
        r"""
        Parameters
        ----------
        b_expr, g_expr, r_expr : str or sympy.core.expr.Expr
            The brightness of the 3 color channels blue, green and red respectively.
            The return values will be cliped to stay in the range [0, 1].
            The value is 0 for min brightness and 1 for the max.
            If the expression gives a complex, take the real part.
            The variables that can be used in these functions are the following:

                * t : The time in seconds since the beginning of the video.
                * i : The relative position along the vertical axis (numpy convention).
                    This value evolves between -1 and 1.
                * j : The relative position along the horizontal axis (numpy convention).
                    This value evolves between -1 and 1.
        shape : tuple or list, optional
            The pixel dimensions of the generated frames.
            The convention adopted is the numpy convention (height, width)
        """
        # check
        assert isinstance(b_expr, (str, Expr)), b_expr.__class__.__name__
        assert isinstance(g_expr, (str, Expr)), g_expr.__class__.__name__
        assert isinstance(r_expr, (str, Expr)), r_expr.__class__.__name__
        assert isinstance(shape, (tuple, list)), shape.__class__.__name__
        assert len(shape) == 2, shape
        assert all(isinstance(s, numbers.Integral) and s > 0 for s in shape)

        # declaration
        self._colors = [None, None, None]
        self._height, self._width = int(shape[0]), int(shape[1])

        # parsing + check
        for i, color in enumerate((b_expr, g_expr, r_expr)):
            if isinstance(color, str):
                color = parse_color(color)
            if (excess := color.free_symbols - set(SYMBOLS.values())):
                raise ValueError(
                    f"the symbols {excess} are not among the possible choices: {SYMBOLS}"
                )
            self._colors[i] = color

        # delegation
        out_streams = [_StreamVideoEquation(self)]
        super().__init__(out_streams)

    @classmethod
    def default(cls):
        return cls(
            "atan(pi*j)/pi + 1/2", # dark blue on the left and bright on the right
            "t*sin(2*pi(i-1/2*t))**2/10", # horizontal descending green waves
            "exp(-(i**2+j**2)/(2*(1e-3+.1*t)))", # red spot in the center that grows
        )

    def getstate(self) -> dict:
        return {
            "b_expr": str(self.b_expr),
            "g_expr": str(self.g_expr),
            "r_expr": str(self.r_expr),
            "shape": self.shape,
        }

    def setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        keys = {"b_expr", "g_expr", "r_expr", "shape"}
        assert set(state) == keys, set(state)-keys
        b_expr = sympify(state["b_expr"], locals=SYMBOLS, evaluate=False)
        g_expr = sympify(state["g_expr"], locals=SYMBOLS, evaluate=False)
        r_expr = sympify(state["r_expr"], locals=SYMBOLS, evaluate=False)
        shape = state["shape"]
        GeneratorVideoEquation.__init__(self, b_expr, g_expr, r_expr, shape)

    @property
    def b_expr(self) -> Expr:
        """
        ** The luminosity expression for the blue channel. **
        """
        return self._colors[0]

    @property
    def g_expr(self) -> Expr:
        """
        ** The luminosity expression for the green channel. **
        """
        return self._colors[1]

    @property
    def r_expr(self) -> Expr:
        """
        ** The luminosity expression for the red channel. **
        """
        return self._colors[2]

    @property
    def shape(self) -> list[int, int]:
        """
        ** The vertical and horizontal (i, j) resolution of the image. **
        """
        return [self._height, self._width]


class _StreamVideoEquation(StreamVideo):
    """
    ** Color field parameterized by time and position. **
    """

    is_space_continuous = True
    is_time_continuous = True

    def __init__(self, node: GeneratorVideoEquation):
        assert isinstance(node, GeneratorVideoEquation), node.__class__.__name__
        super().__init__(node)

        # compilation
        self._colors_func = None

    def _get_colors_func(self) -> typing.Callable:
        """
        ** Allows to "compile" equations at the last moment. **
        """
        if self._colors_func is None:
            self._colors_func = lambdify(
                [SYMBOLS["t"], SYMBOLS["i"], SYMBOLS["j"]],
                [self.node.b_expr, self.node.g_expr, self.node.r_expr],
                modules="numpy",
                cse=True,
            )
        return self._colors_func

    def _snapshot(self, timestamp: float) -> FrameVideo:
        # calculation
        i_field, j_field = np.meshgrid(
            np.linspace(-1, 1, self.height, dtype=np.float32),
            np.linspace(-1, 1, self.width, dtype=np.float32),
            indexing="ij",
            copy=False,
        )
        with warnings.catch_warnings(record=True): # catch numpy warning: divide by zero
            try:
                colors = self._get_colors_func()(timestamp, i_field, j_field)
            except ZeroDivisionError:
                colors = np.full((3, self.height, self.width), np.nan)

        # correction + cast
        frame = FrameVideo(timestamp, self.height, self.width, 3)
        for i, col in enumerate(colors):
            if isinstance(col, numbers.Number): # case expr is cst
                col = torch.full((self.height, self.width), col)
            else:
                col = torch.Tensor(col)
            if col.dtype.is_complex:
                col = torch.real(col) # takes real part
            col = col.to(dtype=torch.float32, copy=False)
            torch.nan_to_num( # replace +inf -inf and nan
                col,
                nan=127.0/255.0,
                posinf=1.0,
                neginf=0.0,
                out=col,
            )
            torch.clip(col, 0.0, 1.0, out=col)
            torch.multiply(col, 255, out=col)
            torch.round(col, out=col)
            col = col.to(dtype=torch.uint8, copy=False)
            frame[:, :, i] = col

        return frame


def parse_color(color: str) -> Expr:
    """
    ** Allows to convert a string into a sympy equation. **

    Parameters
    ----------
    color : str
        The string representation of the equation.
        Some operators like multiplication can be implicit.

    Returns
    -------
    sympy.core.expr.Expr
        sympy.core.expr.Expr

    Raises
    ------
    SyntaxError
        If the entered expression does not allow to properly define an equation.

    Examples
    --------
    >>> from movia.core.generation.video.equation import parse_color
    >>> parse_color("1/2 + 1/2*cos(2pi(t - i*j))")
    cos(pi*(-2*i*j + 2*t))/2 + 1/2
    >>>
    """
    assert isinstance(color, str), color.__class__.__name__

    transformations = standard_transformations + (implicit_multiplication,)
    try:
        color = parse_expr(
            color, local_dict=SYMBOLS, transformations=transformations, evaluate=True
        )
    except (tokenize.TokenError, TypeError) as err:
        raise SyntaxError from err
    if not isinstance(color, Expr):
        raise SyntaxError(f"need to be expression, not {color.__class__.__name__}")
    return color
