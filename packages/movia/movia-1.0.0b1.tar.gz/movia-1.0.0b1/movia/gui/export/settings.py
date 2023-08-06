#!/usr/bin/env python3

"""
** Interactive window for help to choose the export settings. **
----------------------------------------------------------------
"""


import abc
import ast
import logging
import multiprocessing.pool
import pathlib
import re
import stat

import black
from PyQt6 import QtCore, QtGui, QtWidgets

from movia.core.compilation.export.compatibility import (CodecInfos, EncoderInfos, MuxerInfos,
    WriteInfos)
from movia.core.compilation.export.default import suggest_export_params
from movia.core.compilation.graph_to_ast import graph_to_ast
from movia.core.compilation.tree_to_graph import tree_to_graph
from movia.core.io.write import ContainerOutputFFMPEG
from movia.gui.base import MoviaWidget
from movia.gui.tools import WaitCursor


# General classes for limit redundency.

class ComboBox(MoviaWidget, QtWidgets.QComboBox):
    """
    ** Main class for uniformization of QComboBox. **
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        self.currentTextChanged.connect(self.text_changed)

        self.setSizeAdjustPolicy(QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.InsertAtBottom)

    @abc.abstractmethod
    def _text_changed(self, name):
        """
        ** Apply the changes. **
        """
        raise NotImplementedError

    def text_changed(self, element):
        """
        ** The action when a new element is selected. **
        """
        if not element: # for avoid catching self.clear()
            return
        pattern = r"(?P<name>[a-z0-9_\-]{2,})([\s:]+.*)?"
        name = re.fullmatch(pattern, element)["name"]
        self._text_changed(name)


class CoupleLabelWidget(MoviaWidget, QtWidgets.QWidget):
    """
    ** Add a label a the left to a widget. **
    """

    def __init__(self, parent, label_txt, widget_class):
        super().__init__(parent)
        self._parent = parent

        self.widget = widget_class(self) # Instanciate a MoviaWidget child.
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(QtWidgets.QLabel(label_txt, self), 0, 0)
        grid_layout.addWidget(self.widget, 0, 1)
        self.setLayout(grid_layout)

    def refresh(self):
        self.widget.refresh()


class DocViewer(MoviaWidget, QtWidgets.QWidget):
    """
    ** Allows to show and hide a documentation. **
    """

    def __init__(self, parent, doc_getter: callable):
        super().__init__(parent)
        self._parent = parent
        self.doc_getter = doc_getter

        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        self._doc_label = QtWidgets.QLabel(scroll_area)
        font = QtGui.QFont("", -1)
        font.setFixedPitch(True)
        if not QtGui.QFontInfo(font).fixedPitch():
            logging.warning("no fixed pitch font found")
        self._doc_label.setFont(font)
        scroll_area.setWidget(self._doc_label)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(QtWidgets.QLabel("Documentation:", self), 0, 0)
        layout.addWidget(scroll_area, 0, 1)
        self.setLayout(layout)

    def refresh(self):
        """
        ** Update the doc content and displaying. **
        """
        doc_content = self.doc_getter(self)
        self._doc_label.setText(doc_content)
        if doc_content:
            self.show()
        else:
            self.hide()


# Classes about container, muxer choice and parameters.

class MuxerComboBox(ComboBox):
    """
    ** Lists the availables muxers. **
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._muxers_cache = None

    def _text_changed(self, name):
        if self.app.export_settings["muxer"] != name:
            with WaitCursor(self.parent.parent):
                self.app.export_settings["muxer"] = name
                print(f"update muxer: {self.app.export_settings['muxer']}")
                if name != "default":
                    suffix = sorted(MuxerInfos(name).extensions)
                    suffix = suffix.pop(0) if len(suffix) >= 1 else ""
                else:
                    suffix = ""
                if self.app.export_settings["suffix"] != suffix:
                    self.app.export_settings["suffix"] = suffix
                    print(f"update export suffix: {self.app.export_settings['suffix']}")
                self.parent.parent.refresh() # WindowsExportSettings

    def available_muxers(self):
        """
        ** Set of muxers supporting the different types of streams, for a given codecs set. **
        """
        codecs_types = (
            {codec for codec in self.app.export_settings["codecs"] if codec != "default"},
            {stream.type for stream in self.app.tree().in_streams},
        )
        if self._muxers_cache is None or self._muxers_cache[0] != codecs_types:
            muxers = list(WriteInfos().muxers) # frozen the iteration order
            with multiprocessing.pool.ThreadPool() as pool:
                self._muxers_cache = (
                codecs_types,
                    {
                        muxer for muxer, ok in zip(
                            muxers,
                            pool.imap(
                                (lambda muxer: (
                                    codecs_types[1].issubset(set(MuxerInfos(muxer).default_codecs))
                                    and MuxerInfos(muxer).contains_encodecs(codecs_types[0]))
                                ),
                                muxers
                            )
                        ) if ok
                    },
                )
        return self._muxers_cache[1]

    def refresh(self):
        """
        ** Updates the list with the available muxers. **
        """
        self.clear()
        self.addItem(self.app.export_settings["muxer"])
        for muxer in ["default"] + sorted(self.available_muxers()):
            if muxer == self.app.export_settings["muxer"]:
                continue
            self.addItem(muxer) # QtGui.QIcon.fromTheme("video-x-generic")


class FileNameSelector(MoviaWidget, QtWidgets.QWidget):
    """
    ** File manager for select the filename. **
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        self._textbox = QtWidgets.QLineEdit(self)
        self._textbox.textChanged.connect(self._validate_path)

        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(self._textbox, 0, 0)
        button = QtWidgets.QPushButton("Select", self)
        button.clicked.connect(self.filename_dialog)
        grid_layout.addWidget(button, 0, 1)
        self.setLayout(grid_layout)

    def _validate_path(self, new_path):
        """
        ** Try to validate the new path if it is valid. **
        """
        try:
            self.update_path(new_path)
        except AssertionError:
            self._textbox.setStyleSheet("background:red;")
        else:
            self._textbox.setStyleSheet("background:none;")

    def filename_dialog(self):
        """
        ** Opens a window to choose a new file name. **
        """
        new_path, _ = QtWidgets.QFileDialog.getSaveFileName(self)
        if new_path:
            try:
                self.update_path(new_path)
            except AssertionError as err:
                QtWidgets.QMessageBox.warning(
                    None, "Invalid filename", f"Unable to change the filename {new_path} : {err}"
                )

    def update_path(self, new_path):
        """
        ** Check that the new path is correct and set the new path in the settings. **
        """
        with WaitCursor(self.parent.parent):
            assert isinstance(new_path, str), new_path.__class__.__name__
            new_path = pathlib.Path(new_path)
            assert not new_path.is_dir(), new_path
            assert new_path.parent.is_dir(), new_path
            assert new_path.suffix == "" or any(
                new_path.suffix == suf
                for mux in self.parent.muxer_combo_box.available_muxers()
                for suf in MuxerInfos(mux).extensions
            ), f"suffix {new_path.suffix} not allow"

            modif = False

            if self.app.export_settings["parent"] != str(new_path.parent):
                modif = True
                self.app.export_settings["parent"] = str(new_path.parent)
                print(f"update directory: {self.app.export_settings['parent']}")
            if self.app.export_settings["stem"] != new_path.stem:
                modif = True
                self.app.export_settings["stem"] = new_path.stem
                print(f"update file stem: {self.app.export_settings['stem']}")
            if new_path.suffix != self.app.export_settings["suffix"]:
                modif = True
                self.app.export_settings["suffix"] = new_path.suffix
                print(f"update suffix: {self.app.export_settings['suffix']}")
                if new_path.suffix:
                    self.app.export_settings["muxer"] = MuxerInfos.from_suffix(new_path.suffix).name
                    print(f"update muxer: {self.app.export_settings['muxer']}")

            if modif:
                self.parent.parent.refresh() # WindowsExportSettings

    def refresh(self):
        """
        ** Updates the displayed path. **
        """
        new_text = (
            f"{self.app.export_settings['parent']}/{self.app.export_settings['stem']}"
            f"{self.app.export_settings['suffix']}"
        )
        self._textbox.setStyleSheet("background:none;")
        self._textbox.setText(new_text)


class ContainerSettings(MoviaWidget, QtWidgets.QWidget):
    """
    ** Settings of the container file. **
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        self.filename_selector = FileNameSelector(self)
        self.muxer_combo_box = MuxerComboBox(self)
        self.muxer_doc_viewer = DocViewer(
            self,
            lambda w: (
                "" if (muxer := w.app.export_settings["muxer"]) == "default"
                else MuxerInfos(muxer).doc
            )
        )
        self.muxer_doc_viewer.hide()

        layout = QtWidgets.QGridLayout()
        self.init_title(layout)
        layout.addWidget(QtWidgets.QLabel("Path:", self), 1, 0)
        layout.addWidget(self.filename_selector, 1, 1)
        layout.addWidget(QtWidgets.QLabel("Muxer:", self), 2, 0)
        layout.addWidget(self.muxer_combo_box, 2, 1)
        layout.addWidget(self.muxer_doc_viewer, 3, 0, 1, 2)
        self.setLayout(layout)

    def init_title(self, layout):
        """
        ** The section title. **
        """
        title = QtWidgets.QLabel("Muxer Settings")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold")
        layout.addWidget(title, 0, 0, 1, 2)

    def refresh(self):
        self.filename_selector.refresh()
        self.muxer_combo_box.refresh()
        self.muxer_doc_viewer.refresh()


# Classes about codec and encoder.

class CodecComboBox(ComboBox):
    """
    ** Lists the availables codecs. **
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._codecs_cache = None

    def _text_changed(self, name):
        index = self.parent.index
        if self.app.export_settings["codecs"][index] != name:
            self.app.export_settings["codecs"][index] = name
            print(f"update codec (stream {index}): {self.app.export_settings['codecs'][index]}")
            self.parent.encoder_combo_box.text_changed("default")
            self.parent.parent.refresh() # WindowsExportSettings

    def available_codecs(self):
        """
        ** Set of codecs supporting for this streams. **

        Takes in account the muxer and the stream type.
        """
        muxer = self.app.export_settings["muxer"]
        if self._codecs_cache is None or self._codecs_cache[0] != muxer:
            if muxer == "default":
                codecs = WriteInfos().codecs
            else:
                codecs = MuxerInfos(muxer).codecs
            stream_type = self.parent.stream.type
            codecs = {codec for codec in codecs if CodecInfos(codec).type == stream_type}
            self._codecs_cache = (muxer, codecs)
        return self._codecs_cache[1]

    def refresh(self):
        """
        ** Updates the list with the available codecs. **
        """
        self.clear()
        codec = self.app.export_settings["codecs"][self.parent.index]
        if codec != "default" and codec not in self.available_codecs():
            self.text_changed("default")
            return
        self.addItem(codec)
        for codec_ in ["default"] + sorted(self.available_codecs()):
            if codec_ == codec:
                continue
            self.addItem(codec_)


class EncoderComboBox(ComboBox):
    """
    ** Lists the availables encoders. **
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._encoders_cache = None

    def _text_changed(self, name):
        index = self.parent.index
        if self.app.export_settings["encoders"][index] != name:
            self.app.export_settings["encoders"][index] = name
            print(f"update encoder (stream {index}): {self.app.export_settings['encoders'][index]}")
            self.parent.parent.refresh() # WindowsExportSettings

    def available_encoders(self):
        """
        ** Set of encoders supporting for this streams. **

        Takes in account the codec. Trys the real compatibility with the muxer.
        """
        codec = self.app.export_settings["codecs"][self.parent.index]
        muxer = self.app.export_settings["muxer"]
        if self._encoders_cache is None or self._encoders_cache[0] != (codec, muxer):
            if codec == "default":
                encoders = set()
            else:
                encoders = CodecInfos(codec).encoders
            if muxer != "default":
                encoders = list(encoders) # frozen the iteration order
                encoders = {
                    e for e, ok in zip(
                        encoders, WriteInfos().check_compatibilities(encoders, [muxer]).ravel()
                    ) if ok
                }
            self._encoders_cache = ((codec, muxer), encoders)
        return self._encoders_cache[1]

    def refresh(self):
        """
        ** Updates the list with the available encoders. **
        """
        self.clear()
        encoder = self.app.export_settings["encoders"][self.parent.index]
        if encoder != "default" and encoder not in self.available_encoders():
            self.text_changed("default")
            return
        self.addItem(encoder)
        for encoder_ in ["default"] + sorted(self.available_encoders()):
            if encoder_ == encoder:
                continue
            self.addItem(encoder_)


class EncoderSettings(MoviaWidget, QtWidgets.QWidget):
    """
    ** Able to choose and edit the encoder for a given stream. **
    """

    def __init__(self, parent, stream):
        super().__init__(parent)
        self._parent = parent
        self.stream = stream

        self.codec_combo_box = CodecComboBox(self)
        self.encoder_label = QtWidgets.QLabel("Encoder:", self)
        self.encoder_label.hide()
        self.encoder_combo_box = EncoderComboBox(self)
        self.encoder_combo_box.hide()
        self.encoder_doc_viewer = DocViewer(
            self,
            lambda doc_viewer: (
                "" if (
                    encoder := doc_viewer.app.export_settings["encoders"][doc_viewer.parent.index]
                ) == "default" else EncoderInfos(encoder).doc
            )
        )
        self.encoder_doc_viewer.hide()

        layout = QtWidgets.QGridLayout()
        self.init_title(layout)
        layout.addWidget(QtWidgets.QLabel("Codec:", self), 1, 0)
        layout.addWidget(self.codec_combo_box, 1, 1)
        layout.addWidget(self.encoder_label, 2, 0)
        layout.addWidget(self.encoder_combo_box, 2, 1)
        layout.addWidget(self.encoder_doc_viewer, 3, 0, 1, 2)
        self.setLayout(layout)

    @property
    def index(self):
        """
        ** The input stream index of the container output. **
        """
        for index, stream in enumerate(self.app.tree().in_streams):
            if stream is self.stream:
                return index
        raise KeyError(f"the stream {self.stream} is missing in the container output")

    def init_title(self, layout):
        """
        ** The section title. **
        """
        title = QtWidgets.QLabel(f"Stream {self.index} Encoder Settings ({self.stream.type})")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold")
        layout.addWidget(title, 0, 0, 1, 2)

    def refresh(self):
        self.codec_combo_box.refresh()
        self.encoder_combo_box.refresh()
        if self.app.export_settings["codecs"][self.index] == "default":
            self.encoder_label.hide()
            self.encoder_combo_box.hide()
        else:
            self.encoder_label.show()
            self.encoder_combo_box.show()
        self.encoder_doc_viewer.refresh()


# Main class

class WindowsExportSettings(MoviaWidget, QtWidgets.QDialog):
    """
    ** Show the exportation settings. **
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        with WaitCursor(self.main_window):

            self._container_settings = ContainerSettings(self)
            self._encoders = [
                EncoderSettings(self, stream) for stream in self.app.tree().in_streams
            ]

            self.setWindowTitle("Export settings")

            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(self._container_settings)
            for encoder in self._encoders:
                separador = QtWidgets.QFrame()
                separador.setFrameShape(QtWidgets.QFrame.Shape.HLine)
                layout.addWidget(separador)
                layout.addWidget(encoder)
            self.init_next(layout)
            self.setLayout(layout)

            self.refresh()

    def export(self):
        """
        ** Compile to python, close main windows and excecute the new file. **
        """
        self.accept()
        streams = self.app.tree().in_streams
        filename, streams_settings, container_settings = suggest_export_params(
            streams,
            filename=(
                pathlib.Path(self.app.export_settings["parent"]) / self.app.export_settings["stem"]
            ),
            muxer=self.app.export_settings["muxer"],
            encodecs=[
                c if e == "default" else e
                for c, e in zip(
                    self.app.export_settings["codecs"], self.app.export_settings["encoders"]
                )
            ],
        )
        tree = ContainerOutputFFMPEG(
            streams,
            filename=filename,
            streams_settings=streams_settings,
            container_settings=container_settings,
        )
        code = ast.unparse(graph_to_ast(tree_to_graph(tree)))
        code = "#!/usr/bin/env python3\n\n" + code
        code = black.format_str(code, mode=black.Mode())

        # write file and give execution permission
        filename = filename.with_suffix(".py")
        with open(filename, "w", encoding="utf-8") as code_file:
            code_file.write(code)
        filename.chmod(filename.stat().st_mode | stat.S_IEXEC)

        # close
        self.main_window.close()

    def init_next(self, layout):
        """
        ** The button for the next stape. **
        """
        separador = QtWidgets.QFrame()
        separador.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        layout.addWidget(separador)
        button = QtWidgets.QPushButton("Let's Go!")
        button.clicked.connect(self.export)
        layout.addWidget(button)

    def refresh(self):
        with WaitCursor(self):
            self._container_settings.refresh()
            for enc in self._encoders:
                enc.refresh()
