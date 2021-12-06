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

    def _create_label_with_lineedit(self, title, text):
        lb_amplitude = self._create_label(title)
        le_amplitude = self._create_lineedit(text)
        return lb_amplitude, le_amplitude

    def _init_controls(self):
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.setAlignment(QtCore.Qt.AlignLeft)
        tmp_widget = QtWidgets.QWidget()
        tmp_widget.setLayout(h_layout)

        self._lb_amplitude, self._le_amplitude = self._create_label_with_lineedit('Amplitude', '')
        h_layout.addWidget(self._lb_amplitude)
        h_layout.addWidget(self._le_amplitude)

        self.layout().addWidget(tmp_widget)

        self._pb_calculate = QtWidgets.QPushButton()
        self._pb_calculate.setFixedSize(self._pb_width, self._pb_height)
        self._pb_calculate.setText('Test')

        self.layout().addWidget(self._pb_calculate)
