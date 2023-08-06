#!/usr/bin/env python3

"""
** Definition of the toolbar. **
--------------------------------
"""

import numbers
import queue
import subprocess
import sys
import time

import numpy as np
from PyQt6 import QtCore, QtGui, QtWidgets

from movia.core.classes.frame_audio import FrameAudio
from movia.core.classes.frame_video import FrameVideo
from movia.core.classes.stream_audio import StreamAudio
from movia.core.classes.stream_video import StreamVideo
from movia.core.compilation.export.rate_audio import find_optimal_audio_rate
from movia.core.compilation.export.rate_video import find_optimal_video_rate
from movia.core.exceptions import OutOfTimeRange
from movia.core.io.write import frame_audio_to_av, global_scheduler
from movia.gui.base import MoviaWidget



class AudioPlayer(QtCore.QThread):
    """
    ** Allows to play sound buffers in the background, without blocking. **
    """

    def __init__(self, parent):
        super().__init__(parent)

        self._channels = 1 # is quicklely overwriten
        self._buff = queue.Queue()
        self._restart = False
        self._is_alive = True
        self._samplerate = 44100 # is quickely overwriten

    def get_channels(self) -> int:
        """
        ** The numbers of audio channels. **
        """
        return self._channels

    def set_channels(self, new_channels: numbers.Integral):
        """
        ** Updates the number of channels and recreate a new ffmpeg connection. **
        """
        assert isinstance(new_channels, numbers.Integral), new_channels.__class__.__name__
        assert new_channels > 0, new_channels
        new_channels = int(new_channels)
        if new_channels != self.get_channels():
            self._channels = new_channels
            self.restart()

    def restart(self):
        """
        ** Allows to reset link with the sound card. **
        """
        while True:
            try:
                self._buff.get_nowait()
            except queue.Empty:
                break
        self._restart = True
        while self._restart:
            continue

    def run(self):
        """
        ** Allows interaction with the sound card. **
        """
        while self._is_alive:
            cmd = [
                "ffmpeg",
                "-v", "error",
                "-f", "f32le", # means 32 bit input
                "-acodec", "pcm_f32le", # means raw 32 bit input
                "-ar", str(self.get_samplerate()),
                "-ac", str(self.get_channels()),
                "-i", "pipe:",
                "-c:a", "copy", "-bufsize:a", "1024",
                "-f", "pulse",
                "-name", "movia",
                "-buffer_size", "1024", # in bytes or "-buffer_duration", "20", # in ms
                "movia",
            ]
            with subprocess.Popen(
                cmd,
                bufsize=1024,
                stdin=subprocess.PIPE,
                stdout=sys.stdout,
                stderr=sys.stderr
            ) as process:
                with process.stdin as stdin:
                    while self._is_alive and not self._restart:
                        try:
                            data = self._buff.get(timeout=0.02) # 20 ms
                        except queue.Empty:
                            continue
                        stdin.write(data)
            self._restart = False

    def get_samplerate(self) -> int:
        """
        ** The audio signal sampling frequency in Hz. **
        """
        return self._samplerate

    def set_samplerate(self, new_samplerate: numbers.Integral):
        """
        ** Updates the samplerate and recreate a new ffmpeg connection. **
        """
        assert isinstance(new_samplerate, numbers.Integral), new_samplerate.__class__.__name__
        assert new_samplerate > 0, new_samplerate
        new_samplerate = int(new_samplerate)
        if new_samplerate != self.get_samplerate():
            self._samplerate = new_samplerate
            self.restart()

    def stop(self):
        """
        ** Sets run flag to False and waits for thread to finish. **
        """
        self._is_alive = False
        while self.isRunning():
            continue

    @QtCore.pyqtSlot(int, int, bytes)
    def update_audio_frame(self, channels, samplerate, audio_data):
        """
        ** Adds the new samples to the buffer. **
        """
        self.set_channels(channels)
        self.set_samplerate(samplerate)
        self._buff.put(audio_data)


class ReaderThread(MoviaWidget, QtCore.QThread):
    """
    ** Allows to play the video in the background without blocking the rest of the interface. **

    The decorators @property and @attr.setter are not always working.
    """

    change_audio_frame = QtCore.pyqtSignal(int, int, bytes)
    change_video_frame = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        self._frame_iter = None # the audio and video frame generator
        self._frame_iter_signature = None # the signature of the context at the _frame_iter creation
        self._is_alive = True
        self._pause = True
        self._start_timestamp = 0 # the timestamp of the first frames yielden by _frame_iter
        self._start_date = time.time() # the date of the last modification of _start_timestamp

    def get_frame_iter(self):
        """
        ** Return an updated frame generator in the current context. **

        The iterator frames starts yielded from the current time, not nescessary from 0 seconds.
        """
        # context recovery
        streams, rates = [], []
        container_out = self.app.tree()
        if self.get_index_audio() != -1:
            streams.append(
                [s for s in container_out.in_streams if isinstance(s, StreamAudio)]
                [self.get_index_audio()]
            )
            rates.append(find_optimal_audio_rate(streams[-1]))
        if self.get_index_video() != -1:
            streams.append(
                [s for s in container_out.in_streams if isinstance(s, StreamVideo)]
                [self.get_index_video()]
            )
            rates.append(find_optimal_video_rate(streams[-1]))
        position = self.get_position()

        # estimation if need to recreate an iterator
        recreate = False
        if self._frame_iter is None:
            recreate = True
        else:
            signature = hash((tuple(id(s) for s in streams), tuple(rates), position))
            if signature != self._frame_iter_signature:
                self._frame_iter_signature = signature
                recreate = True

        # creation of the new iterator
        if recreate:
            self._frame_iter = iter(global_scheduler(
                streams, rates, start_time=position, duration=0.2
            ))

    def get_index_audio(self):
        """
        ** Retrive the index of the audio stream. **
        """
        if any(isinstance(s, StreamAudio) for s in self.app.tree().in_streams):
            return 0
        return -1

    def get_index_video(self):
        """
        ** Retrive the index of the video stream. **
        """
        if any(isinstance(s, StreamVideo) for s in self.app.tree().in_streams):
            return 0
        return -1

    def is_start(self):
        """
        ** True if we are decoding frames. **
        """
        return (not self._pause) and self.isRunning()

    def get_position(self) -> numbers.Real:
        """
        ** Returns the position in second (read). **
        """
        return self._start_timestamp

    def set_position(self, new_position: numbers.Real):
        """
        ** Sets the position in second (write). **
        """
        assert isinstance(new_position, numbers.Real), new_position.__class__.__name__
        self._start_timestamp = float(new_position)
        self._start_date = time.time()
        self._frame_iter = None # force update

    def refresh(self):
        if self.is_start():
            self.set_pause()
            self.refresh()
            self.set_start()
        else:
            self._frame_iter = None # force update
            cv_img = np.array([[[]]], dtype=np.uint8)
            if (index := self.get_index_video()) != -1:
                container_out = self.app.tree()
                stream = [s for s in container_out.in_streams if isinstance(s, StreamVideo)][index]
                try:
                    frame = stream.snapshot(self.get_position())
                except OutOfTimeRange:
                    frame = stream.snapshot(np.nan) # default frame
                cv_img = frame.to_numpy_bgr(contiguous=True)
            self.change_video_frame.emit(cv_img)

    def run(self):
        """
        ** Sends the frames of the video at the right time. **
        """
        while self._is_alive:

            # wait situation
            if self._pause:
                time.sleep(0.01) # 10 ms
                continue

            # decode next frame
            if self._frame_iter is None:
                self.get_frame_iter() # relatively slow function
            try:
                _, frame = next(self._frame_iter)
            except StopIteration:
                self.set_pause()
                self.set_position(0)
                continue
            if isinstance(frame, FrameVideo):
                emit_func = self.change_video_frame.emit
                data = (frame.to_numpy_bgr(contiguous=True),)
            elif isinstance(frame, FrameAudio):
                emit_func = self.change_audio_frame.emit
                data = (
                    frame.channels,
                    frame.rate,
                    b"".join(bytes(p) for p in frame_audio_to_av(frame).planes),
                    # bytes(frame.numpy(force=True).astype(np.float32).ravel(order="F"))
                )
            else:
                raise NotImplementedError(f"{frame.__class__.__name__} is not yet supported")

            # real time delivery
            timestamp = self.get_position() + (time.time() - self._start_date) # real time position
            wait = frame.time - timestamp
            if wait < 0: # if we are late
                self._start_date -= wait # we don't accumulate it
            else: # but if we are in advance
                time.sleep(wait) # we stay in real time
            emit_func(*data)

    @QtCore.pyqtSlot(float)
    def set_duration_delta(self, d_t: float):
        """
        ** Changes current position. **
        """
        assert isinstance(d_t, float), d_t.__class__.__name__
        if self.is_start():
            current_pos = self.get_position() + (time.time() - self._start_date)
            new_position = max(0, current_pos + d_t)
            self.set_position(new_position)
        else:
            new_position = max(0, self.get_position() + d_t)
            self.set_position(new_position)
            self.refresh()

    @QtCore.pyqtSlot()
    def set_pause(self):
        """
        ** Stops reading. **
        """
        self.set_position(self.get_position() + (time.time() - self._start_date))
        self._pause = True
        self.parent.act_start_pause.setIcon(QtGui.QIcon.fromTheme("media-playback-start"))
        self.parent.act_start_pause.setText("start")

    @QtCore.pyqtSlot()
    def set_start(self):
        """
        ** Starts reading. **
        """
        self._start_date = time.time()
        self._pause = False
        self.parent.act_start_pause.setIcon(QtGui.QIcon.fromTheme("media-playback-pause"))
        self.parent.act_start_pause.setText("pause")

    @QtCore.pyqtSlot()
    def set_stop(self):
        """
        ** Pause and return to the beginning. **
        """
        self.set_pause()
        self.set_position(0)
        self.refresh()

    def stop(self):
        """
        ** Sets run flag to False and waits for thread to finish. **
        """
        self._is_alive = False
        while self.isRunning():
            continue


class VideoViewer(MoviaWidget, QtWidgets.QWidget):
    """
    ** Allows you to play a video and audio stream. **
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent
        self.destroyed.connect(lambda: self.__del__()) # the shortcut ``self.__del__`` does not work

        # declaration
        self._zoom = True
        self.view = QtWidgets.QGraphicsView(QtWidgets.QGraphicsScene(), self)
        self.view.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        self.view.setOptimizationFlag(
            QtWidgets.QGraphicsView.OptimizationFlag.DontAdjustForAntialiasing
        )

        # create the threads
        self.audio_player = AudioPlayer(self)
        self.audio_player.start()
        self.reader_thread = ReaderThread(self)
        self.reader_thread.change_audio_frame.connect(self.audio_player.update_audio_frame)
        self.reader_thread.change_video_frame.connect(self.update_video_frame)
        self.reader_thread.start()

        # create toolbar
        toolbar = QtWidgets.QToolBar()

        self.act_start_pause = QtGui.QAction(self)
        self.reader_thread.set_pause() # updates the icon
        self.act_start_pause.triggered.connect(self.set_start_pause)
        self.act_start_pause.setShortcut("space")
        toolbar.addAction(self.act_start_pause)

        act_backward = QtGui.QAction(QtGui.QIcon.fromTheme("media-seek-backward"), "backward", self)
        act_backward.triggered.connect(lambda: self.reader_thread.set_duration_delta(-10.0))
        toolbar.addAction(act_backward)

        act_pause = QtGui.QAction(QtGui.QIcon.fromTheme("media-playback-stop"), "stop", self)
        act_pause.triggered.connect(self.reader_thread.set_stop)
        toolbar.addAction(act_pause)

        act_forward = QtGui.QAction(QtGui.QIcon.fromTheme("media-seek-forward"), "forward", self)
        act_forward.triggered.connect(lambda: self.reader_thread.set_duration_delta(10.0))
        toolbar.addAction(act_forward)

        toolbar.addSeparator()

        act_zoom_fit = QtGui.QAction(QtGui.QIcon.fromTheme("zoom-fit-best"), "zoom fit best", self)
        act_zoom_fit.triggered.connect(self.set_zoom_fit)
        toolbar.addAction(act_zoom_fit)
        act_zoom_original = QtGui.QAction(
            QtGui.QIcon.fromTheme("zoom-original"), "zoom original", self
        )
        act_zoom_original.triggered.connect(self.set_zoom_original)
        toolbar.addAction(act_zoom_original)

        # location
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.addWidget(toolbar)
        self.setLayout(layout)

    def __del__(self):
        """
        ** Kills processes cleanly. **
        """
        self.reader_thread.stop()
        self.audio_player.stop()

    def convert_cv_qt(self, cv_img):
        """
        ** Convert and rescale from an opencv image to QPixmap. **
        """
        h_in, w_in, ch_in = cv_img.shape
        qt_img = QtGui.QImage(
            cv_img.data, w_in, h_in, ch_in*w_in, QtGui.QImage.Format.Format_BGR888
        )
        if self._zoom:
            width, height = self.view.width()-2, self.view.height()-2
            qt_img = qt_img.scaled(
                width,
                height,
                QtCore.Qt.AspectRatioMode.KeepAspectRatio, # no stretching
                QtCore.Qt.TransformationMode.SmoothTransformation, # bilinear filtering
            )
        return QtGui.QPixmap.fromImage(qt_img)

    def set_start_pause(self):
        """
        ** Switches between start and pause mode. **
        """
        if self.reader_thread.is_start():
            self.reader_thread.set_pause()
        else:
            self.reader_thread.set_start()

    def set_zoom_fit(self):
        """
        ** Allows to adapt the size of the video to the size of the viewer. **
        """
        print("zoom fit best")
        self._zoom = True

    def set_zoom_original(self):
        """
        ** Allows you to adapt the size of the video to the size of the frame. **
        """
        print("zoom original")
        self._zoom = False

    def refresh(self):
        self.reader_thread.refresh()

    @QtCore.pyqtSlot(np.ndarray)
    def update_video_frame(self, cv_img):
        """
        ** Updates the view with a new opencv image. **
        """
        if cv_img.size == 0:
            self.view.scene().clear()
            return
        qt_img = self.convert_cv_qt(cv_img)
        self.view.scene().clear() # avoids the memory leak which consists in superimposing images
        self.view.scene().setSceneRect(0, 0, qt_img.width(), qt_img.height()) # to center the image
        self.view.scene().addPixmap(qt_img)
