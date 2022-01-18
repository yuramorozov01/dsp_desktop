from PyQt5 import QtWidgets

from widgets.fourier_transform_widget import FourierTransformWidget
from widgets.harmonic_signal_widget import HarmonicSignalWidget


class OperationsTabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent):
        super(OperationsTabWidget, self).__init__(parent)
        self._title = 'Basic DSP operations'
        self.setFixedSize(parent.width(), parent.height())
        self._init_tabs()

    def _init_tabs(self):
        child_tab_widgets = {
            'Harmonic signal': HarmonicSignalWidget,
            'Fourier transform': FourierTransformWidget,
        }
        for title, widget in child_tab_widgets.items():
            widget_inst = widget(self, title)
            widget_inst.setFixedSize(self.width(), self.height())
            self.addTab(widget_inst, title)
