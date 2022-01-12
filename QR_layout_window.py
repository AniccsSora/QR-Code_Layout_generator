from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QLineEdit,
                             QHBoxLayout, QVBoxLayout, QSlider,
                             QListWidgetItem, QListWidget, QColorDialog,
                             QFileDialog)
from PyQt5.QtGui import QPixmap, QFont, QIcon, QImage, QColor
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
import math
import QR_layout
from PIL import Image

class QRLayoutGeneratorWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.__uniform_font = QFont('Arial Rounded MT', 15)

        #### Layout 區 ####
        self.main_layout = QHBoxLayout()  # 最外層
        self.qr_code_display_layout = QVBoxLayout()  # QR layout & 拉桿的 layout.
        self.under_qr_code_display_layout_horizontal = QHBoxLayout()  # 接在 layout 圖片下
        self.parameter_layout = QVBoxLayout()  # 設定 QR 相關參數的 layout
        self.parameter_module_horizon = QHBoxLayout() # QR 粗細,


        #### 元件宣告區 ####
        # 建立一個 label，這是用來放 Layout 圖片的。
        self.qr_code_image = QLabel(self)
        # 文字顯示元件
        self.version_text = QLabel(self)  # 顯示 version 號
        # Version 選擇拉條
        self.version_select_slider = QSlider(Qt.Horizontal, self)
        # version edit text area
        self.slider_version_text_area = QLineEdit(self)
        # version Text
        self.slider_version_text = QLabel(self)
        # QR layout 參數 label
        self.module_pixels = QLabel(self)
        self.bold_thickness = QLabel(self)
        self.setting_padding_label = QLabel(self)

        # QR 參數
        # module 大小
        self.module_pixels_text_minus_btn = QPushButton(self)
        self.module_pixels_text_plus_btn = QPushButton(self)
        # 間隔線粗細
        self.bold_thickness_minus_btn = QPushButton(self)
        self.bold_thickness_plus_btn = QPushButton(self)
        # quite zone padding 數量
        self.setting_padding_text_minus_btn = QPushButton(self)
        self.setting_padding_text_plus_btn = QPushButton(self)

        # Qr Code layout 顏色選項
        self.qr_code_color_parameter_list = QListWidget(self)

        # 生成按鈕
        self.generate_btn = QPushButton(self)

        #### 參數區 ####
        self.__version = 8

        # module size pixel
        self.__each_module_pixels = 16

        # 間格條粗細
        self.__divide_bold = 1

        # padding 大小
        self.__padding_module_size = 4

        # QR layout 的各個顏色 與其對應的 Item
        self.qr_color_item_info = \
             [{'name': 'Quite Zone', 'color': (255, 253, 218), 'item': None},
              {'name': 'Find pattern low', 'color': (178, 16, 22), 'item': None},
              {'name': 'Find pattern high', 'color': (248, 161, 164), 'item': None},
              {'name': 'Find pattern while zone', 'color': (255, 255, 255), 'item': None},
              {'name': 'Format zone', 'color': (0, 255, 0), 'item': None},
              {'name': 'Version zone', 'color': (0, 0, 255), 'item': None},
              {'name': 'Data zone', 'color': (192, 192, 192), 'item': None},
              {'name': 'Align low', 'color': (49, 108, 140), 'item': None},
              {'name': 'Align high', 'color': (87, 223, 214), 'item': None},
              {'name': 'Timing low', 'color': (122, 41, 123), 'item': None},
              {'name': 'Timing high', 'color': (237, 211, 237), 'item': None},
              {'name': 'Dark module', 'color': (0, 0, 0), 'item': None},
              {'name': 'Divide', 'color': (158, 157, 153), 'item': None}]
        # 根據上方的字典做設定
        for item_info in self.qr_color_item_info:
            item_name = item_info['name']
            color = item_info['color']
            item_info['item'] = QListWidgetItem(item_name)

        # setup ui
        self.init_ui()


    def init_ui(self):
        #### 各 layout 設定 ####
        # main_layout
        self.main_layout.addStretch(5)  # 彈簧
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.addLayout(self.qr_code_display_layout, 10)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.addStretch(2)
        self.main_layout.addLayout(self.parameter_layout)
        self.main_layout.addStretch(5)

        # qr_code_display_layout, 放置輸出圖片的 layout
        self.qr_code_display_layout.addWidget(self.version_text)  # 加入 version 說明
        self.qr_code_display_layout.addStretch(100)  # 強制把 text 頂到最上面
        self.qr_code_display_layout.addWidget(self.qr_code_image)  # 加入Qr 圖片
        self.qr_code_display_layout.addLayout(self.under_qr_code_display_layout_horizontal)
        self.qr_code_display_layout.addStretch(100)

        # under_qr_code_display_layout_horizontal, version 選擇器
        self.under_qr_code_display_layout_horizontal.setContentsMargins(0, 10, 0, 20)
        self.under_qr_code_display_layout_horizontal.addWidget(self.slider_version_text)
        self.under_qr_code_display_layout_horizontal.addWidget(self.slider_version_text_area)
        self.under_qr_code_display_layout_horizontal.addWidget(self.version_select_slider)
        self.slider_version_text.setFont(QFont(QFont('Arial Rounded MT', 15)))

        # self.parameter_layout, qr code 參數設定 layout
        self.parameter_layout.setContentsMargins(50, 50, 50, 50)
        self.parameter_layout.addLayout(self.parameter_module_horizon)
        self.parameter_layout.addWidget(self.qr_code_color_parameter_list)
        self.parameter_layout.addWidget(self.generate_btn)

        # self.parameter_module_horizon: module 數值設定區
        self.parameter_module_horizon.setContentsMargins(0, 0, 0, 10)
        # 模組大小設定
        self.parameter_module_horizon.addWidget(self.module_pixels)
        self.parameter_module_horizon.addWidget(self.module_pixels_text_minus_btn)
        self.parameter_module_horizon.addWidget(self.module_pixels_text_plus_btn)
        # 間隔線粗度
        self.parameter_module_horizon.addWidget(self.bold_thickness)
        self.parameter_module_horizon.addWidget(self.bold_thickness_minus_btn)
        self.parameter_module_horizon.addWidget(self.bold_thickness_plus_btn)
        # Quite padding 數量
        self.parameter_module_horizon.addWidget(self.setting_padding_label)
        self.parameter_module_horizon.addWidget(self.setting_padding_text_minus_btn)
        self.parameter_module_horizon.addWidget(self.setting_padding_text_plus_btn)


        #### 元件設定區、賦數值區 ####

        # qr_code_display
        #_qr_img = QPixmap('aaa.jpg').scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        _qr_img = self.get_qr_code_layout_image()
        self.qr_code_image.setPixmap(_qr_img)  # 給圖片
        self.qr_code_image.resize(540, 540)  # 調整 label 的 size

        # version text， 左上的，不可編輯
        # self.version_text.setMargin(100)
        self.version_text.setFont(QFont('Arial Rounded MT', 15))
        self.version_text.setAutoFillBackground(True)
        self.version_text.setContentsMargins(10, 10, 10, 10)
        self.version_text.adjustSize()

        # self.slider_version_text 文字設定
        self.slider_version_text.setFont(QFont('Arial Rounded MT', 15))
        self.slider_version_text.setText("Version : ")

        # self.slider_version_text_area 輸入文字區域設定，左下可以輸入的
        self.slider_version_text_area.setText(str(self.__version))
        self.slider_version_text_area.setMaximumHeight(self.slider_version_text.sizeHint().height() * 1.6)
        self.slider_version_text_area.setMaximumWidth(self.slider_version_text.sizeHint().width())
        self.slider_version_text_area.setFont(QFont('Arial Rounded MT', 15))
        self.slider_version_text_area.editingFinished.connect(self.slider_version_text_area_editingFinished)

        # self.version_select_slider 設定
        self.version_select_slider.setMinimum(1)
        self.version_select_slider.setMaximum(40)
        self.version_select_slider.setFixedHeight(50)
        self.version_select_slider.setValue(self.__version)
        self.update_version(self.__version)
        self.version_select_slider.valueChanged.connect(self.version_slide_change)

        # qr layout 參數相關設定

        # self.module_pixels
        self.module_pixels.setText("Module: {}".format(self.__each_module_pixels))
        self.module_pixels.setFont(self.__uniform_font)

        # self.module_pixels_text_minus_btn
        self.module_pixels_text_minus_btn.clicked.connect(self.module_pixels_text_minus_btn_clicked)
        self.module_pixels_text_minus_btn.setFont(self.__uniform_font)
        self.module_pixels_text_minus_btn.setText("−")
        self.module_pixels_text_minus_btn.setFixedWidth(50)

        # self.module_pixels_text_plus_btn
        self.module_pixels_text_plus_btn.clicked.connect(self.module_pixels_text_plus_btn_clicked)
        self.module_pixels_text_plus_btn.setFont(self.__uniform_font)
        self.module_pixels_text_plus_btn.setText("+")
        self.module_pixels_text_plus_btn.setFixedWidth(50)

        # self.bold_thickness
        self.bold_thickness.setFont(self.__uniform_font)

        # self.bold_thickness_minus_btn
        self.bold_thickness_minus_btn.clicked.connect(self.bold_thickness_minus_btn_clicked)
        self.bold_thickness_minus_btn.setFont(self.__uniform_font)
        self.bold_thickness_minus_btn.setText("−")
        self.bold_thickness_minus_btn.setFixedWidth(50)

        # self.bold_thickness_plus_btn
        self.bold_thickness_plus_btn.clicked.connect(self.bold_thickness_plus_btn_clicked)
        self.bold_thickness_plus_btn.setFont(self.__uniform_font)
        self.bold_thickness_plus_btn.setText("+")
        self.bold_thickness_plus_btn.setFixedWidth(50)


        #  self.bold_thickness
        self.bold_thickness.setText("Bold: {}".format(self.__divide_bold))

        # self.setting_padding_label
        self.setting_padding_label.setText("Pad: {}".format(self.__padding_module_size))
        self.setting_padding_label.setFont(self.__uniform_font)

        # self.setting_padding_text_minus_btn
        self.setting_padding_text_minus_btn.setText("−")
        self.setting_padding_text_minus_btn.setFixedWidth(50)
        self.setting_padding_text_minus_btn.clicked.connect(self.setting_padding_text_minus_btn_clicked)

        # self.setting_padding_text_plus_btn
        self.setting_padding_text_plus_btn.setText("+")
        self.setting_padding_text_plus_btn.setFixedWidth(50)
        self.setting_padding_text_plus_btn.clicked.connect(self.setting_padding_text_plus_btn_clicked)

        # self.qr_code_color_parameter_list, qr layout 顏色相關設定 item list
        self.qr_code_color_parameter_list.setMinimumWidth(500)
        self.qr_code_color_parameter_list.itemClicked.connect(self.list_widget_clicked)

        # 各個 color item widget
        for idx, item in enumerate(self.qr_color_item_info):
            item['item'].setIcon(self.get_color_icon(item['color']))
            self.qr_code_color_parameter_list.insertItem(idx, item['item'])

        # 生成
        self.generate_btn.setText("Generate")
        self.generate_btn.clicked.connect(self.go_generate_qrcode_layout)
        self.generate_btn.setFont(self.__uniform_font)

        #### 總 Layout 設定 ####
        # 總 layout 給他加入到 QWidget 上.
        self.setLayout(self.main_layout)
        self.setWindowTitle("QR Code Layout Generator")
        self.move(400, 100)
        self.resize(self.sizeHint())  # can get a proper size automatically
        self.show()

    def update_version(self, version):
        self.__version = version
        self.version_text.setText("Version : {}".format(self.__version)) # , "像素", "像素"
        self.slider_version_text_area.setText(str(self.__version))
        self.slider_version_text_area.setMaximumHeight(self.slider_version_text.sizeHint().height() * 1.6)
        self.slider_version_text_area.setMaximumWidth(self.slider_version_text.sizeHint().width())


    @staticmethod
    def get_color_icon(c, size=13, bold=1, bold_color=(0, 0, 0)):
        r, g, b = c[0], c[1], c[2]
        np_map = np.zeros((size, size, 3), dtype=np.uint8)
        np_map[:, :, 0] = r
        np_map[:, :, 1] = g
        np_map[:, :, 2] = b
        pad_thick = ((bold, bold), (bold, bold))
        _ir = np.pad(np_map[:, :, 0], pad_thick, constant_values=bold_color[0])
        _ig = np.pad(np_map[:, :, 1], pad_thick, constant_values=bold_color[1])
        _ib = np.pad(np_map[:, :, 2], pad_thick, constant_values=bold_color[2])
        aa = np.dstack((_ir, _ig, _ib))
        bold_icon = QImage(aa[:], aa.shape[1], aa.shape[0],
                           aa.shape[1]*3,  # bytesPerLine 不能省略...
                           QImage.Format_RGB888)
        q_map = QPixmap(bold_icon)
        return QIcon(q_map)

    def list_widget_clicked(self, item):
        print("====================")
        self  # let charm alert shut up!
        target_idx = None
        print(item.text() + " Pick up!")
        for idx, target in enumerate(self.qr_color_item_info):
            if target['name'] == item.text():
                target_idx = idx
                break  # must to be run, or raise exception
        else:
            # if above break executed, is shown correct data flow.
            raise Exception("self.qr_color_item_info \"{}\"NOT exists".format(item.text()))

        print("before color:", self.qr_color_item_info[target_idx]['color'])
        _r, _g, _b = self.qr_color_item_info[target_idx]['color'][0], \
                     self.qr_color_item_info[target_idx]['color'][1], \
                     self.qr_color_item_info[target_idx]['color'][2]
        color = QColorDialog.getColor(QColor(_r, _g, _b))  # 叫出調色板
        if color.isValid():
            hex_rgb = color.name().lstrip('#')
            rgb_888 = tuple(int(hex_rgb[i:i + 2], 16) for i in (0, 2, 4))
            self.qr_color_item_info[target_idx]['color'] = rgb_888
            item.setIcon(self.get_color_icon(rgb_888))
            self.update_qr_code_layout()
        else:
            print("No change")

        print("after color:", self.qr_color_item_info[target_idx]['color'])
        print("================ End of select color")

    def version_slide_change(self):
        self.update_version(self.version_select_slider.value())
        self.update_qr_code_layout()

    def slider_version_text_area_editingFinished(self: QWidget):
        #
        origin_version = self.__version
        current_str = self.slider_version_text_area.text()
        current_str = current_str.replace(" ", "")

        if current_str.isnumeric():
            v = math.floor(int(current_str))
            if 1 <= v <= 40:
                self.update_version(v)
                self.version_select_slider.setValue(v)
            else:  # 超過 1~40
                self.slider_version_text_area.setText(str(origin_version))
        else:  # 輸入非數字
            self.slider_version_text_area.setText(str(origin_version))

    def update_qr_code_layout(self):
        new_layout = self.get_qr_code_layout_image()
        print("Each_module_pixels :", self.__each_module_pixels )
        self.qr_code_image.setPixmap(new_layout)

    def get_qr_code_layout_image(self, just_get_image_and_no_update_window_layout=False, rescale=500):

        kwargs = {
            'version': self.__version,
            'c_quite_zone': self.get_rgb_color_by_item_display_name("Quite Zone"),
            'c_find_pattern_low': self.get_rgb_color_by_item_display_name("Find pattern low"),
            'c_find_pattern_high': self.get_rgb_color_by_item_display_name("Find pattern high"),
            'c_find_pattern_while_zone': self.get_rgb_color_by_item_display_name("Find pattern while zone"),
            'c_format_zone': self.get_rgb_color_by_item_display_name("Format zone"),
            'c_version_zone': self.get_rgb_color_by_item_display_name("Version zone"),
            'c_data_zone': self.get_rgb_color_by_item_display_name("Data zone"),
            'c_align_low': self.get_rgb_color_by_item_display_name("Align low"),
            'c_align_high': self.get_rgb_color_by_item_display_name("Align high"),
            'c_timing_low': self.get_rgb_color_by_item_display_name("Timing low"),
            'c_timing_high': self.get_rgb_color_by_item_display_name("Timing high"),
            'c_dark_module': self.get_rgb_color_by_item_display_name("Dark module"),
            'c_divide': self.get_rgb_color_by_item_display_name("Divide"),
            'pixels_per_module': self.__each_module_pixels,
            'divide_bold': self.__divide_bold,
            'len__padding_module': self.__padding_module_size,
        }

        if self.__version == 1:
            kwargs["c_version_zone"] = kwargs['c_data_zone']

        qr_lay_generator = QR_layout.qrBan(**kwargs)
        qr_lay = qr_lay_generator.get_layout()

        if just_get_image_and_no_update_window_layout:
            return qr_lay
        else:
            bold_icon = QImage(qr_lay[:], qr_lay.shape[1], qr_lay.shape[0],
                               qr_lay.shape[1] * 3,  # bytesPerLine 不能省略...
                               QImage.Format_RGB888)

            return QPixmap(bold_icon).scaled(rescale, rescale, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def get_rgb_color_by_item_display_name(self, item_display_name):
        for item in self.qr_color_item_info:
            if item['name'] == item_display_name:
                return item['color']
        else:
            raise Exception(
                "TryAccessNonExistsItemNameColor: Please item name: \'{}\' exists.".format(item_display_name))

    def module_pixels_text_minus_btn_clicked(self):
        self.__each_module_pixels -= 1
        self.__each_module_pixels = 1 if self.__each_module_pixels <= 1 else self.__each_module_pixels
        self.module_pixels.setText("Module: {}".format(self.__each_module_pixels))
        self.update_qr_code_layout()

    def module_pixels_text_plus_btn_clicked(self):
        self.__each_module_pixels += 1
        self.__each_module_pixels = 40 if self.__each_module_pixels >= 40 else self.__each_module_pixels
        self.module_pixels.setText("Module: {}".format(self.__each_module_pixels))
        self.update_qr_code_layout()

    def bold_thickness_minus_btn_clicked(self):
        self.__divide_bold -= 1
        self.__divide_bold = 0 if self.__divide_bold < 0 else self.__divide_bold
        self.bold_thickness.setText("Bold: {}".format(self.__divide_bold))
        self.update_qr_code_layout()

    def bold_thickness_plus_btn_clicked(self):
        self.__divide_bold += 1
        self.__divide_bold = 40 if self.__divide_bold >= 40 else self.__divide_bold
        self.bold_thickness.setText("Bold: {}".format(self.__divide_bold))
        self.update_qr_code_layout()

    def setting_padding_text_minus_btn_clicked(self):
        self.__padding_module_size -= 1
        self.__padding_module_size = 0 if self.__padding_module_size < 0 else self.__padding_module_size
        self.setting_padding_label.setText("Pad: {}".format( self.__padding_module_size))
        self.update_qr_code_layout()

    def setting_padding_text_plus_btn_clicked(self):
        self.__padding_module_size += 1
        self.__padding_module_size = 1 if self.__padding_module_size > 40 else self.__padding_module_size
        self.setting_padding_label.setText("Pad: {}".format(self.__padding_module_size))
        self.update_qr_code_layout()

    def go_generate_qrcode_layout(self):

        layout = self.get_qr_code_layout_image(just_get_image_and_no_update_window_layout=True)
        layout = Image.fromarray(layout)
        fname, ok = QFileDialog.getSaveFileName(self,"檔案儲存",
        "./layout_v_" + str(self.__version),
        "jpg (*.jpg);;bmp (*.bmp);;All files (*.*)")
        if ok :
            layout.save(fname)
            print(fname, ", save complete!")
        else:
            pass