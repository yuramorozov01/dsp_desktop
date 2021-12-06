from PyQt5 import QtCore, QtGui, QtWidgets


class FourierTransformWidget(QtWidgets.QWidget):
    def __init__(self, parent, title):
        super(FourierTransformWidget, self).__init__(parent)
        self.setWindowTitle(title)
