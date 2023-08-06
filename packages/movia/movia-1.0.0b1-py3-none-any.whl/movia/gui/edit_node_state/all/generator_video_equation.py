#!/usr/bin/env python3

"""
** Properties of a ``movia.core.generation.video.equation.GeneratorVideoEquation``. **
--------------------------------------------------------------------------------------
"""

from PyQt6 import QtWidgets

from movia.core.generation.video.equation import SYMBOLS, parse_color
from movia.gui.edit_node_state.base import EditBase
from movia.gui.edit_node_state.interface import Resizable



class EditGeneratorVideoEquation(EditBase):
    """
    ** Allows to view and modify the properties of a node of type ``GeneratorVideoEquation``.
    """

    def __init__(self, parent, node_name):
        super().__init__(parent, node_name)
        self.textboxs = [None, None, None]

        grid_layout = QtWidgets.QGridLayout()
        ref_span = Resizable(self)(grid_layout)
        self.init_expr(grid_layout, ref_span=ref_span)
        self.setLayout(grid_layout)

    def _validate_b(self, text):
        return self.update_color(text, 0)

    def _validate_g(self, text):
        return self.update_color(text, 1)

    def _validate_r(self, text):
        return self.update_color(text, 2)

    def init_expr(self, grid_layout, ref_span=0):
        """
        ** Displays and allows to modify the equations. **
        """
        colors = ("Blue", "Green", "Red")
        exprs = (str(self.state["b_expr"]), str(self.state["g_expr"]), str(self.state["r_expr"]))
        vals = (self._validate_b, self._validate_g, self._validate_r)
        for i, (color, expr, val) in enumerate(zip(colors, exprs, vals)):
            grid_layout.addWidget(QtWidgets.QLabel(f"{color} Expression:"), ref_span, 0)
            self.textboxs[i] = QtWidgets.QLineEdit()
            self.textboxs[i].setText(expr)
            self.textboxs[i].textChanged.connect(val)
            grid_layout.addWidget(self.textboxs[i], ref_span, 1)
            ref_span += 1
        return ref_span

    def update_color(self, text, color_index):
        """
        ** Check that the formula is correct and update the color. **
        """
        try:
            color = parse_color(text)
        except (SyntaxError, ZeroDivisionError):
            self.textboxs[color_index].setStyleSheet("background:red;")
            return
        if color.free_symbols - set(SYMBOLS.values()):
            self.textboxs[color_index].setStyleSheet("background:red;")
            return

        color_key = ("b_expr", "g_expr", "r_expr")[color_index]
        self.try_set_state(self.get_new_state({color_key: str(color)}), self.textboxs[color_index])
