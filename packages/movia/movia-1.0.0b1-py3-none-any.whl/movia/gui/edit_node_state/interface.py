#!/usr/bin/env python3

"""
** Allows you to avoid redundancy in the node editing windows. **
-----------------------------------------------------------------

Defines several accessors that allow to lighten the code of child classes.
This is also where methods common to several classes are implemented to avoid data redundancy.
"""


from PyQt6 import QtWidgets

from movia.gui.edit_node_state.base import EditBase



class Seedable:
    """
    ** Allows you to manage a `seed` field. **

    It is a float between [0, 1[.
    """

    def __init__(self, edit: EditBase):
        assert isinstance(edit, EditBase), edit.__class__.__name__
        assert "seed" in edit.state, sorted(edit.state)
        self.edit = edit
        self.edit.ref.append(self)
        self.textbox = QtWidgets.QLineEdit(edit)

    def __call__(self, grid_layout: QtWidgets.QGridLayout, ref_span=0):
        """
        ** Displays and allows to modify the av kwargs. **
        """
        assert isinstance(grid_layout, QtWidgets.QGridLayout), grid_layout.__class__.__name__
        grid_layout.addWidget(QtWidgets.QLabel("Seed (0 <= float < 1):", self.edit))
        self.textbox.setText(str(self.edit.state["seed"]))
        self.textbox.textChanged.connect(self.validate)
        grid_layout.addWidget(self.textbox, ref_span, 1)
        ref_span += 1
        return ref_span

    def validate(self, text):
        """
        ** Check that the seed is a float in [0, 1[. **,
        """
        try:
            seed = float(text)
        except ValueError:
            self.textbox.setStyleSheet("background:red;")
            return
        if seed < 0 or seed >= 1:
            self.textbox.setStyleSheet("background:red;")
            return

        self.edit.try_set_state(self.edit.get_new_state({"seed": seed}), self.textbox)


class Resizable:
    """
    ** Allows to change the resolution of the video frames. **
    """

    def __init__(self, edit: EditBase):
        assert isinstance(edit, EditBase), edit.__class__.__name__
        assert "shape" in edit.state, sorted(edit.state)
        self.edit = edit
        self.edit.ref.append(self)
        self.spinbox_h = QtWidgets.QSpinBox(edit)
        self.spinbox_w = QtWidgets.QSpinBox(edit)

    def __call__(self, grid_layout: QtWidgets.QGridLayout, ref_span=0):
        """
        ** Allows to change the size of the images. **
        """
        assert isinstance(grid_layout, QtWidgets.QGridLayout), grid_layout.__class__.__name__

        for val, label, action, spinbox in zip(
            self.edit.state["shape"],
            ("Height", "Width"),
            (self.update_h, self.update_w),
            (self.spinbox_h, self.spinbox_w),
        ):
            grid_layout.addWidget(QtWidgets.QLabel(f"{label} Resolution:", self.edit), ref_span, 0)
            spinbox.setMinimum(1)
            spinbox.setMaximum(2147483647) # maximum admissible limit
            spinbox.setSuffix(" pxl")
            spinbox.setValue(val)
            spinbox.valueChanged.connect(action)
            grid_layout.addWidget(spinbox, ref_span, 1)
            ref_span += 1
        return ref_span

    def update_h(self, height):
        """
        ** Trys to update the new shape. **
        """
        new_shape = [height, self.edit.state["shape"][1]]
        self.edit.try_set_state(self.edit.get_new_state({"shape": new_shape}), self.spinbox_h)

    def update_w(self, width):
        """
        ** Trys to update the new shape. **
        """
        new_shape = [self.edit.state["shape"][0], width]
        self.edit.try_set_state(self.edit.get_new_state({"shape": new_shape}), self.spinbox_w)
