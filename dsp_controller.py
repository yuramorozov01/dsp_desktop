from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot

import sys
import numpy as np

from dsp_view import Ui_mw_dsp


class DspController(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self._init_params()
        self._init_ui_form()
        self._apply_params()

    def _init_params(self):
        self._window_width = 800
        self._window_height = 600

    def _init_ui_form(self):
        self._app = QtWidgets.QApplication(sys.argv)
        self._form = QtWidgets.QMainWindow()
        self._ui = Ui_mw_dsp()
        self._ui.setupUi(self._form)

    def _apply_params(self):
        self._form.setFixedSize(self._window_width, self._window_height)

    def start(self):
        self._update_form()
        sys.exit(self._app.exec_())

    def _update_form(self):
        self._form.hide()
        self._form.show()

    def _msgbox_message(self, title, message):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText(title)
        msg_box.setInformativeText(
            message
        )
        msg_box.exec_()


if __name__ == '__main__':
    dsp_controller = DspController()
    dsp_controller.start()
