import numpy as np
from PyQt5 import QtCore, QtWidgets

from widgets.utils import WidgetsCreator
from widgets.utils import data_utils as utils


class FourierTransformWidget(QtWidgets.QWidget):
    def __init__(self, parent, title):
        super(FourierTransformWidget, self).__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(parent.width(), parent.height())

        self._widgets_creator = WidgetsCreator()

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 25)
        self.setLayout(layout)

        self._init_controls()

    def _init_controls(self):
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

        self._sa_harmonics = self._widgets_creator.create_scroll_area(None)
        self.layout().addWidget(self._sa_harmonics)

        self._pw_polyharmonic_signal, self._plot_polyharmonic_signal = self._widgets_creator.create_graphic(
            np.arange(0, 1),
            np.arange(0, 1)
        )

        self._pw_frequency_spectre_signal, self._plot_frequency_spectre_signal = self._widgets_creator.create_graphic(
            np.arange(0, 1),
            np.arange(0, 1)
        )

        layout_widget = self._widgets_creator.combine_widgets_to_layout(
            self._pw_polyharmonic_signal,
            self._pw_frequency_spectre_signal
        )
        self.layout().addWidget(layout_widget)

        self.layout().addStretch()

    def _update_generated_polyharmonic_signal(self, time, result_values, check_boxes):
        new_values = []
        for i, check_box in enumerate(check_boxes):
            if check_box.checkState():
                new_values.append(result_values[i])
        new_result_values = []
        for j in time:
            res = 0
            for harmonic_values in new_values:
                res += harmonic_values[j]
            new_result_values.append(res)
        self._plot_polyharmonic_signal.setData(time, new_result_values)

    def _pb_generate_on_click(self):
        amplitudes = utils.get_save_data_array_from_lineedit(self._le_amplitudes, value_type=int)
        frequencies = utils.get_save_data_array_from_lineedit(self._le_frequencies, value_type=int)
        amplitudes, frequencies = utils.equalize_length_of_arrays(0, amplitudes, frequencies)

        time_size = 1024

        # fix for Nyquist–Shannon sampling theorem
        if max(frequencies) >= (time_size // 2):
            time_size = (max(frequencies) + 1) * 2

        time, result_values, harmonics_values = utils.generate_polyharmonic_signal(time_size, amplitudes, frequencies)
        self._plot_polyharmonic_signal.setData(time, result_values)

        fft_values = np.fft.fft(result_values)
        int_fft_values = abs(fft_values)
        self._plot_frequency_spectre_signal.setData(time[:(len(time) // 2)], int_fft_values[:(len(time) // 2)])

        check_boxes = []
        combined_layout_widgets = []
        for harmonic_values in harmonics_values:
            plot_widget, plot = self._widgets_creator.create_graphic(
                time,
                harmonic_values
            )
            checkbox = self._widgets_creator.create_checkbox(
                lambda: self._update_generated_polyharmonic_signal(time, harmonics_values, check_boxes)
            )
            check_boxes.append(checkbox)
            combined_layout_widget = self._widgets_creator.combine_widgets_to_layout(plot_widget, checkbox)
            combined_layout_widgets.append(combined_layout_widget)

        all_plots_with_checkboxes_vertical_layout = self._widgets_creator.combine_widgets_to_layout(
            *combined_layout_widgets,
            layout=QtWidgets.QVBoxLayout
        )
        self._sa_harmonics.setWidget(all_plots_with_checkboxes_vertical_layout)
