import numpy as np
import scipy.signal
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

        self._signal_1 = []
        self._signal_2 = []

        self._init_controls()

    def _init_controls(self):
        signal_1_generator_layout = self._widgets_creator.create_signal_widget_generator_layout(
            generate_callback_func=lambda ampls, freqs, amount_of_points, plot: self._pb_generate_on_click(
                ampls,
                freqs,
                amount_of_points,
                plot,
                cache=self._signal_1
            )
        )

        signal_2_generator_layout = self._widgets_creator.create_signal_widget_generator_layout(
            generate_callback_func=lambda ampls, freqs, amount_of_points, plot: self._pb_generate_on_click(
                ampls,
                freqs,
                amount_of_points,
                plot,
                cache=self._signal_2
            )
        )

        signals_generator_layout = self._widgets_creator.combine_widgets_to_layout(
            signal_1_generator_layout,
            signal_2_generator_layout
        )

        self.layout().addWidget(signals_generator_layout)

        pw_correlation_signal, plot_correlation_signal = self._widgets_creator.create_graphic(
            np.arange(0, 1),
            np.arange(0, 1),
            width=self.width(),
        )
        self.layout().addWidget(pw_correlation_signal)

        sld_correlation = self._widgets_creator.create_slider(
            (0, 2047),
            value_changed_callback=lambda value: self._sld_correlation_value_changed(
                value,
                pw_correlation_signal,
                plot_correlation_signal
            )
        )
        self.layout().addWidget(sld_correlation)

        self.layout().addStretch()

    def _pb_generate_on_click(self, src_amplitudes, src_frequencies, src_amount_of_points, plot, cache=None):
        amplitudes = utils.get_save_data_array_from_lineedit(src_amplitudes, value_type=int)
        frequencies = utils.get_save_data_array_from_lineedit(src_frequencies, value_type=int)
        amount_of_points = utils.get_save_data_from_lineedit(src_amount_of_points, value_type=int)

        amplitudes, frequencies = utils.equalize_length_of_arrays(0, amplitudes, frequencies)

        time, result_values, harmonics_values = utils.generate_polyharmonic_signal(
            amount_of_points,
            amplitudes,
            frequencies
        )
        plot.setData(time, result_values)

        if cache is not None:
            cache.clear()
            cache.extend(result_values)

    def _sld_correlation_value_changed(self, value, plot_widget, plot):
        correlation = scipy.signal.correlate(self._signal_1, self._signal_2, mode='full')

        correlation_signal_len = len(self._signal_1) + len(self._signal_2)

        to_visualize = correlation[:value]
        to_visualize = np.pad(
            to_visualize,
            (0, correlation_signal_len - len(to_visualize)),
            mode='constant',
            constant_values=0
        )
        max_abs_value = max(abs(max(correlation)), abs(min(correlation)))
        rect = QtCore.QRectF(0, (-max_abs_value * 2) // 2, correlation_signal_len, max_abs_value * 2)
        plot_widget.setRange(rect)

        plot.setData(range(0, correlation_signal_len), to_visualize)
