import numpy as np
from PyQt5 import QtCore, QtWidgets

from widgets.utils import WidgetsCreator
from widgets.utils import data_utils as utils


class CorrelationWidget(QtWidgets.QWidget):
    def __init__(self, parent, title):
        super(CorrelationWidget, self).__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(parent.width(), parent.height())

        self._widgets_creator = WidgetsCreator()

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 25)
        self.setLayout(layout)

        self._init_controls()

    def _init_controls(self):
        signal_1_generator_layout = self._widgets_creator.create_signal_widget_generator_layout(
            generate_callback_func=self._pb_generate_on_click
        )

        signal_2_generator_layout = self._widgets_creator.create_signal_widget_generator_layout(
            generate_callback_func=self._pb_generate_on_click
        )

        signals_generator_layout = self._widgets_creator.combine_widgets_to_layout(
            signal_1_generator_layout,
            signal_2_generator_layout
        )

        self.layout().addWidget(signals_generator_layout)

        self.layout().addStretch()

    def _pb_generate_on_click(self, src_amplitudes, src_frequencies, plot):
        amplitudes = utils.get_save_data_array_from_lineedit(src_amplitudes, value_type=int)
        frequencies = utils.get_save_data_array_from_lineedit(src_frequencies, value_type=int)
        amplitudes, frequencies = utils.equalize_length_of_arrays(0, amplitudes, frequencies)

        time_size = 1024

        # fix for Nyquist–Shannon sampling theorem
        if max(frequencies) >= (time_size // 2):
            time_size = (max(frequencies) + 1) * 2

        time, result_values, harmonics_values = utils.generate_polyharmonic_signal(time_size, amplitudes, frequencies)
        plot.setData(time, result_values)
