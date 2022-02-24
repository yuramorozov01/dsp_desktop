import numpy as np
import scipy.signal
import cv2
from PyQt5 import QtGui, QtCore, QtWidgets

from widgets.utils import WidgetsCreator
from widgets.utils import data_utils as utils


class ImageCorrelationWidget(QtWidgets.QWidget):
    def __init__(self, parent, title):
        super(ImageCorrelationWidget, self).__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(parent.width(), parent.height())

        self._widgets_creator = WidgetsCreator()

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 25)
        self.setLayout(layout)

        self._source_image_1 = np.array([])
        self._source_image_2 = np.array([])

        self._init_controls()

    def _init_controls(self):
        lb_image_1 = self._widgets_creator.create_label('', width=350, height=450)
        lb_open_image_1, pb_open_image_1, tmp_widget_image_1 = \
            self._widgets_creator.create_label_with_pushbutton(
                'Image 1',
                'Load image',
                callback=lambda: self._pb_open_image_on_click(self._source_image_1, lb_image_1),
                layout='h',
            )
        image_1 = self._widgets_creator.combine_widgets_to_layout(
            tmp_widget_image_1,
            lb_image_1,
            layout='v'
        )

        lb_image_2 = self._widgets_creator.create_label('', width=350, height=450)
        lb_open_image_2, pb_open_image_2, tmp_widget_image_2 = \
            self._widgets_creator.create_label_with_pushbutton(
                'Image 2',
                'Load image',
                callback=lambda: self._pb_open_image_on_click(self._source_image_2, lb_image_2),
                layout='h',
            )
        image_2 = self._widgets_creator.combine_widgets_to_layout(
            tmp_widget_image_2,
            lb_image_2,
            layout='v'
        )

        image_loaders_layout = self._widgets_creator.combine_widgets_to_layout(
            image_1,
            image_2
        )

        self.layout().addWidget(image_loaders_layout)

        self.layout().addStretch()

    def _open_file_name_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            'Load image',
            '',
            'Images (*.jpeg *jpg *png)',
            options=options
        )
        return filename

    def _lb_image_set_image(self, label, image):
        width = 0
        height = 0
        if len(image.shape) == 3:
            height, width, channel = image.shape
        elif len(image.shape) == 2:
            height, width = image.shape
        bytes_per_line = 3 * width
        qimage = QtGui.QImage(image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        if width >= height:
            qimage = qimage.scaledToWidth(label.width())
        else:
            qimage = qimage.scaledToHeight(label.height())
        label.setPixmap(QtGui.QPixmap.fromImage(qimage))

    def _pb_open_image_on_click(self, array_to_load_image, label):
        filename = self._open_file_name_dialog()
        if filename:
            array_to_load_image = cv2.imread(filename, cv2.IMREAD_COLOR)
            cv2.cvtColor(array_to_load_image, cv2.COLOR_BGR2RGB, array_to_load_image)
            self._lb_image_set_image(label, array_to_load_image)
