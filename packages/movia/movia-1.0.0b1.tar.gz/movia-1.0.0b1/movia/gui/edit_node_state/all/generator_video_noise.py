#!/usr/bin/env python3

"""
** Properties of a ``movia.core.generation.video.noise.GeneratorVideoNoise``. **
--------------------------------------------------------------------------------
"""

from PyQt6 import QtWidgets

from movia.gui.edit_node_state.base import EditBase
from movia.gui.edit_node_state.interface import Resizable, Seedable



class EditGeneratorVideoNoise(EditBase):
    """
    ** Allows to view and modify the properties of a generator of type ``GeneratorAudioNoise``.
    """

    def __init__(self, parent, node_name):
        super().__init__(parent, node_name)
        grid_layout = QtWidgets.QGridLayout()
        ref_span = Seedable(self)(grid_layout)
        Resizable(self)(grid_layout, ref_span)
        self.setLayout(grid_layout)
