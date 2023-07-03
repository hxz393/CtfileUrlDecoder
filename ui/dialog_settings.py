"""
这是一个Python文件，其中包含一个类 DialogSettings。

类 DialogSettings 是一个设置对话框，用户可以通过这个对话框修改应用的设置，包括账号token和请求间隔时间。该对话框包含两个选项卡："基本" 和 "高级"，以及两个按钮："确定" 和 "取消"。

在 construct_widgets 函数中，构建了选项卡和按钮。

在 construct_basic_tab 函数中，构建了 "基本" 选项卡，其中包含了账号token的输入框。

在 construct_advanced_tab 函数中，构建了 "高级" 选项卡，其中包含了请求间隔时间的输入框。

在 construct_buttons 函数中，构建了 "确定" 和 "取消" 按钮。

函数 accept 用于接受对话框的修改，并保存配置。

函数 reject 用于拒绝对话框的修改。

这个模块的主要功能是提供用户修改应用设置的界面。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QTabWidget, QWidget, QHBoxLayout

from module import CONFIG_PATH, init_config, write_list_to_file, get_resource_path

logger = logging.getLogger(__name__)


class DialogSettings(QDialog):
    """
    设置对话框。

    :type QDialog: PyQt5.QtWidgets.QDialog
    :param QDialog: PyQt5.QtWidgets.QDialog 的子类
    """

    def __init__(self):
        super(DialogSettings, self).__init__(flags=Qt.Dialog | Qt.WindowCloseButtonHint)

        self.setWindowTitle('设置')
        self.setWindowIcon(QIcon(get_resource_path('media/icons8-setting-26.png')))
        self.setStyleSheet("font-size: 14px;")

        self.config_file = CONFIG_PATH
        try:
            self.user_token, self.user_delay = init_config()
        except Exception as e:
            logger.error(f"Failed to initialize configuration: {e}")
            return

        self.layout = QFormLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.construct_widgets()

    def construct_widgets(self):
        """
        构建选项卡和按钮。

        :rtype: None
        :return: None
        """
        self.tab_widget = QTabWidget(self)
        self.construct_basic_tab()
        self.construct_advanced_tab()

        self.layout.addRow(self.tab_widget)
        self.construct_buttons()

    def construct_basic_tab(self):
        """
        构建 "基本" 选项卡。

        :rtype: None
        :return: None
        """
        self.tab_basic = QWidget()
        self.tab_basic_layout = QFormLayout(self.tab_basic)

        self.input_token = QLineEdit(self.user_token)
        self.input_token.setPlaceholderText("账号认证令牌")

        self.tab_basic_layout.addRow("账号 token", self.input_token)

        self.tab_widget.addTab(self.tab_basic, "基本")

    def construct_advanced_tab(self):
        """
        构建 "高级" 选项卡。

        :rtype: None
        :return: None
        """
        self.tab_advanced = QWidget()
        self.tab_advanced_layout = QFormLayout(self.tab_advanced)

        self.input_delay = QLineEdit(self.user_delay)
        self.input_delay.setValidator(QIntValidator(0, 1000))
        self.input_delay.setPlaceholderText("每次请求间隔")

        self.tab_advanced_layout.addRow("请求间隔（毫秒）", self.input_delay)

        self.tab_widget.addTab(self.tab_advanced, "高级")

    def construct_buttons(self):
        """
        构建确定和取消按钮。

        :rtype: None
        :return: None
        """
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # 创建一个水平布局
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.button_box)
        self.button_layout.setContentsMargins(0, 0, 13, 8)

        self.layout.addRow(self.button_layout)

    def accept(self) -> None:
        """
        接受对话框的修改，并保存配置。

        :rtype: None
        :return: None
        """
        self.config = [self.input_token.text(), self.input_delay.text()]
        try:
            write_list_to_file(self.config_file, self.config)
        except Exception as e:
            logger.error(f"Failed to write to configuration file: {e}")
            return
        super().accept()

    def reject(self) -> None:
        """
        拒绝对话框的修改。

        :rtype: None
        :return: None
        """
        super().reject()
