import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets

from widgets.utils import data_utils
from widgets.utils.widgets_creator import WidgetsCreator


class FourierTransformWidget(QtWidgets.QWidget):
    def __init__(self, parent, title):
        super(FourierTransformWidget, self).__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(parent.width(), parent.height())

        self._widgets_creator = WidgetsCreator()

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(layout)

        self._init_controls()

    def _init_controls(self):
        self._lb_amount_of_signals, self._le_amount_of_signals, tmp_widget = \
            self._widgets_creator.create_label_with_lineedit(
                'Signals',
                '',
                layout=True
            )
        self.layout().addWidget(tmp_widget)

        self._lb_amplitudes, self._le_amplitudes, tmp_widget = self._widgets_creator.create_label_with_lineedit(
            'Amplitudes',
            '',
            layout=True
        )
        self.layout().addWidget(tmp_widget)

        self._lb_frequencies, self._le_frequencies, tmp_widget = self._widgets_creator.create_label_with_lineedit(
            'Frequencies',
            '',
            layout=True
        )
        self.layout().addWidget(tmp_widget)

        self._pb_generate = self._widgets_creator.create_pushbutton('Generate', callback=self._pb_generate_on_click)
        self.layout().addWidget(self._pb_generate)

        self.layout().setContentsMargins(0, 0, 0, 200)

        self._pw_polyharmonic_signal, self._plot_polyharmonic_signal = self._widgets_creator.create_graphic(
            np.arange(0, 1),
            np.arange(0, 1)
        )
        self.layout().addWidget(self._pw_polyharmonic_signal)

        self.layout().addStretch()

    def _pb_generate_on_click(self):
        amount_of_signals = data_utils.get_save_data_from_lineedit(self._le_amount_of_signals, value_type=int)
        amplitudes = data_utils.get_save_data_array_from_lineedit(self._le_amplitudes, value_type=int)
        frequencies = data_utils.get_save_data_array_from_lineedit(self._le_frequencies, value_type=int)

        time = np.arange(0, 1024, 1)
        harmonics_values = []
        for i in range(amount_of_signals):
            harmonics_values.append(amplitudes[i] * np.sin(2 * np.pi * frequencies[i] * time / len(time)))

        result_values = []
        for j in time:
            res = 0
            for harmonic_values in harmonics_values:
                res += harmonic_values[j]
            result_values.append(res)

        self._plot_polyharmonic_signal.setData(time, result_values)
