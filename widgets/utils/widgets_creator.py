import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets


class WidgetsCreator:
    def __init__(self):
        self._init_params()

    def _init_params(self):
        self._lb_width = 80
        self._lb_height = 30

        self._le_width = 80
        self._le_height = 20

        self._pb_width = 100
        self._pb_height = 30

        self._cb_width = 100
        self._cb_height = 30

    def create_label(self, title):
        label = QtWidgets.QLabel()
        label.setFixedSize(self._lb_width, self._lb_height)
        label.setText(title)
        return label

    def create_lineedit(self, text):
        lineedit = QtWidgets.QLineEdit()
        lineedit.setFixedSize(self._le_width, self._le_height)
        lineedit.setText(text)
        return lineedit

    def create_label_with_widget(self, title, lambda_widget_creator=None, layout=False):
        label = self.create_label(title)
        widget = None
        layout_widget = None
        if lambda_widget_creator is not None:
            widget = lambda_widget_creator()
            if layout:
                h_layout = QtWidgets.QHBoxLayout()
                h_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
                layout_widget = QtWidgets.QWidget()
                layout_widget.setLayout(h_layout)
                h_layout.addWidget(label)
                h_layout.addWidget(widget)
                h_layout.setContentsMargins(0, 0, 0, 0)
        return label, widget, layout_widget

    def create_label_with_lineedit(self, title, text, layout=False):
        label, lineedit, layout_widget = self.create_label_with_widget(
            title,
            lambda_widget_creator=lambda: self.create_lineedit(text),
            layout=layout
        )
        return label, lineedit, layout_widget

    def create_pushbutton(self, text, callback=None):
        pushbutton = QtWidgets.QPushButton()
        pushbutton.setFixedSize(self._pb_width, self._pb_height)
        pushbutton.setText(text)
        if callback is not None:
            pushbutton.clicked.connect(callback)
        return pushbutton

    def create_combobox(self, items):
        combobox = QtWidgets.QComboBox()
        combobox.setFixedSize(self._cb_width, self._cb_height)
        for title, value in items.items():
            combobox.addItem(title, userData=value)
        return combobox

    def create_label_with_combobox(self, title, items, layout=False):
        label, combobox, layout_widget = self.create_label_with_widget(
            title,
            lambda_widget_creator=lambda: self.create_combobox(items),
            layout=layout
        )
        return label, combobox, layout_widget

    def create_graphic(self, x, y, width=600, height=200):
        plot_widget = pg.PlotWidget()
        plot = plot_widget.plot(x, y)
        plot_widget.setMaximumWidth(width)
        plot_widget.setMaximumHeight(height)
        return plot_widget, plot
