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

        self._source_image_1 = []
        self._source_image_2 = []
        self._corr_res = []

        self._init_controls()

    def _init_controls(self):
        lb_image_1 = self._widgets_creator.create_label('', width=250, height=350)
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

        lb_image_2 = self._widgets_creator.create_label('', width=250, height=350)
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
            image_2,
            layout='h'
        )

        lb_image_corr_res = self._widgets_creator.create_label('', width=250, height=350)
        lb_found_image_part = self._widgets_creator.create_label('', width=250, height=350)

        images_res = self._widgets_creator.combine_widgets_to_layout(
            lb_image_corr_res,
            lb_found_image_part
        )

        lb_correlate, pb_correlate, tmp_widget_corr_res = \
            self._widgets_creator.create_label_with_pushbutton(
                'Correlation',
                'Correlate',
                callback=lambda: self._pb_correlate_on_click(self._corr_res, lb_image_corr_res, lb_found_image_part),
                layout='h',
            )
        image_corr_res = self._widgets_creator.combine_widgets_to_layout(
            tmp_widget_corr_res,
            images_res,
            layout='v'
        )

        res_widget = self._widgets_creator.combine_widgets_to_layout(
            image_loaders_layout,
            image_corr_res,
            layout='h'
        )

        self.layout().addWidget(res_widget)

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

    def _lb_image_set_image(self, label, image, grayscale=False):
        width = 0
        height = 0
        if len(image.shape) == 3:
            height, width, channel = image.shape
        elif len(image.shape) == 2:
            height, width = image.shape
        bytes_per_line = 3 * width
        qimage = QtGui.QImage(image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        if grayscale:
            qimage = QtGui.QImage(image.data, width, height, 1 * width, QtGui.QImage.Format_Grayscale8)
        if (width > label.width()) or (height > label.height()):
            if width >= height:
                qimage = qimage.scaledToWidth(label.width())
            else:
                qimage = qimage.scaledToHeight(label.height())
        label.setPixmap(QtGui.QPixmap.fromImage(qimage))

    def _pb_open_image_on_click(self, array_to_load_image, label):
        filename = self._open_file_name_dialog()
        if filename:
            array_to_load_image.clear()
            loaded_image = cv2.imread(filename, cv2.IMREAD_COLOR)
            cv2.cvtColor(loaded_image, cv2.COLOR_BGR2RGB, loaded_image)
            array_to_load_image += list(loaded_image)
            self._lb_image_set_image(label, loaded_image)

    def _pb_correlate_on_click(self, array_to_save_image, label_for_image, label_for_found_image):
        im_1_copy_np = np.array(self._source_image_1.copy())
        im_2_copy_np = np.array(self._source_image_2.copy())

        im_1_copy_np = cv2.cvtColor(im_1_copy_np, cv2.COLOR_RGB2GRAY)
        im_2_copy_np = cv2.cvtColor(im_2_copy_np, cv2.COLOR_RGB2GRAY)

        corr_res = utils.normxcorr2(im_2_copy_np, im_1_copy_np, mode='same')

        array_to_save_image.clear()
        array_to_save_image += list(corr_res)

        self._lb_image_set_image(label_for_image, utils.normalize_image(corr_res), grayscale=True)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(corr_res)

        w, h = im_2_copy_np.shape[::-1]

        top_left = max_loc
        top_left = (top_left[0] - w // 2, top_left[1] - h // 2)

        bottom_right = (top_left[0] + w, top_left[1] + h)

        res_copy = np.array(self._source_image_1.copy())
        cv2.rectangle(res_copy, top_left, bottom_right, (255, 0, 0), 10)

        self._lb_image_set_image(label_for_found_image, res_copy)
