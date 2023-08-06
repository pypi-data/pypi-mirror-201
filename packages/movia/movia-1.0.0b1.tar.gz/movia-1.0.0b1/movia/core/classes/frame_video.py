#!/usr/bin/env python3

"""
** Defines the structure a video frame. **
------------------------------------------
"""


import numbers

import numpy as np
import torch

from movia.core.classes.frame import Frame



class FrameVideo(Frame):
    """
    ** An image with time information for video context. **

    Behaves like a torch tensor of shape (height, width, nbr_channels).
    The shape is consistent with pyav and cv2.
    The dtype is automaticaly cast into torch.uint8.

    Parameters
    ----------
    channels : int
        The numbers of layers (readonly).
    height : int
        The dimension i (vertical) of the image in pxl (readonly).
    time : numbers.Real
        The time of the frame inside the video stream in second (readonly).
    width : int
        The dimension j (horizontal) of the image in pxl (readonly).
    """

    def __new__(cls, time: numbers.Real, *args, **kwargs):
        assert isinstance(time, numbers.Real), time.__class__.__name__
        frame = super().__new__(cls, *args, metadata=time, **kwargs)
        frame = frame.to(dtype=torch.uint8, copy=False)
        assert frame.ndim == 3, frame.shape
        assert frame.shape[0] > 0, frame.shape
        assert frame.shape[1] > 0, frame.shape
        assert frame.shape[2] in {1, 3, 4}, frame.shape
        assert frame.dtype == torch.uint8, frame.dtype
        return frame

    @property
    def channels(self) -> int:
        """
        ** The numbers of layers. **

        Examples
        --------
        >>> from movia.core.classes.frame_video import FrameVideo
        >>> FrameVideo(0, 480, 720, 3).channels
        3
        >>>
        """
        return self.shape[2]

    @property
    def height(self) -> int:
        """
        ** The dimension i (vertical) of the image in pxl. **

        Examples
        --------
        >>> from movia.core.classes.frame_video import FrameVideo
        >>> FrameVideo(0, 480, 720, 3).height
        480
        >>>
        """
        return self.shape[0]

    @property
    def time(self) -> numbers.Real:
        """
        ** The time of the frame inside the video stream in second. **

        Examples
        --------
        >>> from movia.core.classes.frame_video import FrameVideo
        >>> FrameVideo(0, 480, 720, 3).time
        0
        >>>
        """
        return self.metadata

    def to_numpy_bgr(self, contiguous=False) -> np.ndarray[np.uint8]:
        """
        ** Returns the 3 channels numpy frame representation. **

        Parameters
        ----------
        contiguous : boolean, default=False
            If True, guaranti that the returned numpy array is c-contiguous.

        Examples
        --------
        >>> from movia.core.classes.frame_video import FrameVideo
        >>> frame = FrameVideo(0, 480, 720, 3).to_numpy_bgr() # classical bgr
        >>> type(frame), frame.shape, frame.dtype
        (<class 'numpy.ndarray'>, (480, 720, 3), dtype('uint8'))
        >>> frame = FrameVideo(0, 480, 720, 1).to_numpy_bgr() # grayscale
        >>> type(frame), frame.shape, frame.dtype
        (<class 'numpy.ndarray'>, (480, 720, 3), dtype('uint8'))
        >>> frame = FrameVideo(0, 480, 720, 4).to_numpy_bgr() # alpha channel
        >>> type(frame), frame.shape, frame.dtype
        (<class 'numpy.ndarray'>, (480, 720, 3), dtype('uint8'))
        >>>
        """
        assert isinstance(contiguous, bool), contiguous.__class__.__name__
        frame_np = self.numpy(force=True)
        depth = frame_np.shape[2]
        if depth == 1: # grayscale
            frame_np = np.tile(frame_np, 3)
        elif depth == 4: # remove alpha channel
            frame_np = frame_np[..., :3]
        if contiguous:
            return np.ascontiguousarray(frame_np)
        return frame_np

    @property
    def width(self) -> int:
        """
        ** The dimension j (horizontal) of the image in pxl. **

        Examples
        --------
        >>> from movia.core.classes.frame_video import FrameVideo
        >>> FrameVideo(0, 480, 720, 3).width
        720
        >>>
        """
        return self.shape[1]
