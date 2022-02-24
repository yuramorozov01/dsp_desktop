import numpy as np
from PyQt5 import QtCore, QtWidgets

from widgets.utils import WidgetsCreator
from widgets.utils import data_utils as utils


class HarmonicSignalWidget(QtWidgets.QWidget):
    def __init__(self, parent, title):
        super(HarmonicSignalWidget, self).__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(parent.width(), parent.height())

        self._widgets_creator = WidgetsCreator()

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(layout)

        self._init_controls()

    def _init_controls(self):
        self._lb_amplitude, self._le_amplitude, layout_widget = self._widgets_creator.create_label_with_lineedit(
            'Amplitude',
            '',
            layout='h'
        )
        self.layout().addWidget(layout_widget)

        self._lb_frequency, self._le_frequency, layout_widget = self._widgets_creator.create_label_with_lineedit(
            'Frequency',
            '',
            layout='h'
        )
        self.layout().addWidget(layout_widget)

        items = {
            '0': 0,
            'pi': np.pi,
            '2 * pi': 2 * np.pi,
            'pi / 2': np.pi / 2,
            'pi / 3': np.pi / 3,
            'pi / 4': np.pi / 4,
            'pi / 5': np.pi / 5,
            'pi / 6': np.pi / 6,
            '2 * pi / 3': 2 * np.pi / 3,
            '3 * pi / 4': 3 * np.pi / 4,
        }
        self._lb_initial_phases, self._cb_initial_phases, layout_widget = \
            self._widgets_creator.create_label_with_combobox(
                'Phase',
                items,
                layout='h'
            )
        self.layout().addWidget(layout_widget)

        self._pb_generate = self._widgets_creator.create_pushbutton('Generate', callback=self._pb_generate_on_click)
        self.layout().addWidget(self._pb_generate)

        self.layout().setContentsMargins(0, 0, 0, 0)

        self._pw_harmonic_signal, self._plot_harmonic_signal = self._widgets_creator.create_graphic(
            np.arange(0, 1),
            np.arange(0, 1),
            width=800,
            height=400
        )
        self.layout().addWidget(self._pw_harmonic_signal)

        self.layout().addStretch()

    def _pb_generate_on_click(self):
        amplitude = utils.get_save_data_from_lineedit(self._le_amplitude, value_type=int)
        frequency = utils.get_save_data_from_lineedit(self._le_frequency, value_type=int)
        initial_phase = self._cb_initial_phases.itemData(self._cb_initial_phases.currentIndex())

        time = np.arange(0, 1024, 1)
        harmonic_values = amplitude * np.sin((2 * np.pi * frequency * time / len(time)) + initial_phase)
        self._plot_harmonic_signal.setData(time, harmonic_values)
