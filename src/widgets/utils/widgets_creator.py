import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
from widgets.utils.figure_canvas import FigureCanvas


class WidgetsCreator:
    def __init__(self):
        self._init_params()

    def _init_params(self):
        self._lb_width = 80
        self._lb_height = 30

        self._le_width = 120
        self._le_height = 20

        self._pb_width = 100
        self._pb_height = 30

        self._cb_width = 100
        self._cb_height = 30

    def create_label(self, title, width=None, height=None):
        label = QtWidgets.QLabel()
        label.setFixedSize(width or self._lb_width, height or self._lb_height)
        label.setText(title)
        return label

    def create_lineedit(self, text):
        lineedit = QtWidgets.QLineEdit()
        lineedit.setFixedSize(self._le_width, self._le_height)
        lineedit.setText(text)
        return lineedit

    def create_checkbox(self, callback=None):
        checkbox = QtWidgets.QCheckBox()
        checkbox.setChecked(True)
        if callback is not None:
            checkbox.toggled.connect(callback)
        return checkbox

    def _create_label_with_widget(self, title, lambda_widget_creator=None, layout=None):
        label = self.create_label(title)
        widget = None
        layout_widget = None
        if lambda_widget_creator is not None:
            widget = lambda_widget_creator()
            if layout is not None:
                layout_widget = self.combine_widgets_to_layout(label, widget, layout=layout)
        return label, widget, layout_widget

    def create_label_with_lineedit(self, title, text, layout='h'):
        label, lineedit, layout_widget = self._create_label_with_widget(
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

    def create_label_with_combobox(self, title, items, layout='h'):
        label, combobox, layout_widget = self._create_label_with_widget(
            title,
            lambda_widget_creator=lambda: self.create_combobox(items),
            layout=layout
        )
        return label, combobox, layout_widget

    def create_label_with_pushbutton(self, title, text, callback=None, layout=None):
        label, pushbutton, layout_widget = self._create_label_with_widget(
            title,
            lambda_widget_creator=lambda: self.create_pushbutton(text, callback=callback),
            layout=layout
        )
        return label, pushbutton, layout_widget

    def create_graphic(self, x, y, width=600, height=200):
        plot_widget = pg.PlotWidget()
        plot = plot_widget.plot(x, y)
        plot_widget.setMaximumWidth(width)
        plot_widget.setMaximumHeight(height)
        plot_widget.setMinimumWidth(width)
        plot_widget.setMinimumHeight(height)
        return plot_widget, plot

    def create_scroll_area(self, inner_widget, width=900, height=400):
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setAlignment(QtCore.Qt.AlignTop)
        scroll_area.setMaximumWidth(width)
        scroll_area.setMaximumHeight(height)
        scroll_area.setMinimumWidth(width)
        scroll_area.setMinimumHeight(height)
        scroll_area.setWidget(inner_widget)
        return scroll_area

    def create_slider(self, range_value, value_changed_callback=None):
        slider = QtWidgets.QSlider()
        slider.setRange(range_value[0], range_value[1])
        slider.setValue(range_value[0])
        slider.setOrientation(QtCore.Qt.Horizontal)
        if value_changed_callback is not None:
            slider.valueChanged.connect(value_changed_callback)
        return slider

    def combine_widgets_to_layout(self, *widgets, layout='h'):
        layouts = {
            'h': QtWidgets.QHBoxLayout,
            'v': QtWidgets.QVBoxLayout,
        }
        layout = layouts.get(layout)
        layout = layout()
        layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout_widget = QtWidgets.QWidget()
        layout_widget.setLayout(layout)
        for widget in widgets:
            layout.addWidget(widget)
        layout.addStretch()
        return layout_widget

    def create_signal_widget_generator_layout(self, generate_callback_func=None):
        lb_amplitudes_signal, le_amplitudes_signal, amplitudes_widget_signal = self.create_label_with_lineedit(
            'Amplitudes',
            '',
            layout='h'
        )

        lb_frequencies_signal, le_frequencies_signal, frequencies_widget_signal = self.create_label_with_lineedit(
            'Frequencies',
            '',
            layout='h'
        )

        lb_amount_of_points, le_amount_of_points, amount_of_points_widget = self.create_label_with_lineedit(
            'Points',
            '',
            layout='h'
        )

        pw_polyharmonic_signal, plot_polyharmonic_signal = self.create_graphic(
            np.arange(0, 1),
            np.arange(0, 1)
        )

        pb_generate = self.create_pushbutton(
            'Generate',
            callback=lambda: generate_callback_func(
                le_amplitudes_signal,
                le_frequencies_signal,
                le_amount_of_points,
                plot_polyharmonic_signal
            )
        )

        signal_generator_layout = self.combine_widgets_to_layout(
            amplitudes_widget_signal,
            frequencies_widget_signal,
            amount_of_points_widget,
            pb_generate,
            pw_polyharmonic_signal,
            layout='v'
        )

        return signal_generator_layout

    def create_figure_canvas(self):
        figure_canvas = FigureCanvas()
        return figure_canvas
