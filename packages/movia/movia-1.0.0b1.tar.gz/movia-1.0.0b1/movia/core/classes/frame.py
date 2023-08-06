#!/usr/bin/env python3

"""
** Defines the structure of a base frame, inerit from torch array. **
---------------------------------------------------------------------
"""

import logging

import torch



class Frame(torch.Tensor):
    """
    ** A General Frame. **

    Attributes
    ----------
    matadata : object
        Any information to throw during the transformations.
    """

    def __new__(cls, *args, metadata: object=None, **kwargs):
        """
        Parameters
        ----------
        metadata : object
            Any value to throw between the tensor operations.
        *args : tuple
            Forwarded to the `torch.Tensor` initialisator.
        **kwargs : dict
            Forwarded to the `torch.Tensor` initialisator.
        """
        tensor = super().__new__(cls, *args, **kwargs)
        tensor.metadata = metadata
        return tensor

    def __repr__(self):
        """
        ** Allows to add metadata to the display. **

        Examples
        --------
        >>> from movia.core.classes.frame import Frame
        >>> Frame([0.0, 1.0, 2.0], metadata="matadata_value")
        Frame([0., 1., 2.], metadata='matadata_value')
        >>>
        """
        base = super().__repr__()
        return f"{base[:-1]}, metadata={repr(self.metadata)})"

    @classmethod
    def __torch_function__(cls, func, types, args=(), kwargs=None):
        """
        ** Enable to throw `metadata` into the new generations. **

        Examples
        --------
        >>> import torch
        >>> from movia.core.classes.frame import Frame
        >>> frame = Frame(metadata="matadata_value")
        >>> frame.metadata
        'matadata_value'
        >>> torch.sin(frame).metadata # external call
        'matadata_value'
        >>> (frame + 0).metadata # internal method
        'matadata_value'
        >>>
        """
        if kwargs is None:
            kwargs = {}
        result = super().__torch_function__(func, types, args, kwargs)
        if isinstance(result, cls):
            try:
                result.metadata = args[0].metadata # args[0] is self
            except AssertionError:
                logging.warning("unable to transmit metadata")
        return result

    @property
    def shape(self) -> tuple[int]:
        """
        ** Solve pylint error E1136: Value 'self.shape' is unsubscriptable. **
        """
        return tuple(super().shape)
