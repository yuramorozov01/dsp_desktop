import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets


class HarmonicSignalWidget(QtWidgets.QWidget):
    def __init__(self, parent, title):
        super(HarmonicSignalWidget, self).__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(parent.width(), parent.height())

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(layout)

        self._init_params()
        self._init_controls()

    def _init_params(self):
        self._lb_width = 80
        self._lb_height = 30

        self._le_width = 80
        self._le_height = 20

        self._pb_width = 100
        self._pb_height = 30

        self._cb_width = 100
        self._cb_height = 30

    def _create_label(self, title):
        label = QtWidgets.QLabel()
        label.setFixedSize(self._lb_width, self._lb_height)
        label.setText(title)
        return label

    def _create_lineedit(self, text):
        lineedit = QtWidgets.QLineEdit()
        lineedit.setFixedSize(self._le_width, self._le_height)
        lineedit.setText(text)
        return lineedit

    def _create_label_with_lineedit(self, title, text, layout=False):
        label = self._create_label(title)
        lineedit = self._create_lineedit(text)
        if layout:
            h_layout = QtWidgets.QHBoxLayout()
            h_layout.setAlignment(QtCore.Qt.AlignLeft)
            tmp_widget = QtWidgets.QWidget()
            tmp_widget.setLayout(h_layout)
            h_layout.addWidget(label)
            h_layout.addWidget(lineedit)
            h_layout.setContentsMargins(0, 0, 0, 0)
            return label, lineedit, tmp_widget
        return label, lineedit

    def _create_pushbutton(self, text, callback=None):
        pushbutton = QtWidgets.QPushButton()
        pushbutton.setFixedSize(self._pb_width, self._pb_height)
        pushbutton.setText(text)
        if callback is not None:
            pushbutton.clicked.connect(callback)
        return pushbutton

    def _create_graphic(self, x, y):
        plot_widget = pg.PlotWidget()
        plot = plot_widget.plot(x, y)
        return plot_widget, plot

    def _init_controls(self):
        self._lb_amplitude, self._le_amplitude, tmp_widget = self._create_label_with_lineedit('Amplitude',
                                                                                              '',
                                                                                              layout=True)
        self.layout().addWidget(tmp_widget)

        self._lb_frequency, self._le_frequency, tmp_widget = self._create_label_with_lineedit('Frequency',
                                                                                              '',
                                                                                              layout=True)
        self.layout().addWidget(tmp_widget)

        self._pb_generate = self._create_pushbutton('Generate', callback=self._pb_generate_on_click)
        self.layout().addWidget(self._pb_generate)

        self.layout().setContentsMargins(0, 0, 0, 200)

        self._pw_harmonic_signal, self._plot_harmonic_signal = self._create_graphic(np.arange(0, 1), np.arange(0, 1))
        self.layout().addWidget(self._pw_harmonic_signal)

    def _get_save_data_from_lineedit(self, lineedit, value_type=int):
        try:
            value_type = value_type(lineedit.text())
            return value_type
        except ValueError:
            return value_type()

    def _pb_generate_on_click(self):
        amplitude = self._get_save_data_from_lineedit(self._le_amplitude, int)
        frequency = self._get_save_data_from_lineedit(self._le_frequency, int)

        time = np.arange(0, 1024, 1)
        values = amplitude * np.sin(2 * np.pi * frequency * time / len(time))
        self._plot_harmonic_signal.setData(time, values)
