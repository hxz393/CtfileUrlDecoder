"""
这是一个Python文件，其中包含一个类 `ActionAbout`。

类 `ActionAbout` 用于定义 "关于" 动作。它接受一个参数 `main_window`，这是所属的主窗口。在 `__init__` 方法中，我们定义了一个 QAction 对象 `action_about`，并将其与 `open_about` 方法连接。当动作被触发时，`open_about` 方法会尝试打开 "关于" 对话框。

这个模块主要用于定义和实现 "关于" 动作，包括创建动作，设置动作属性和定义动作的触发行为。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import NoReturn

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow

from module.get_resource_path import get_resource_path
from ui.dialog_about import DialogAbout

logger = logging.getLogger(__name__)


# noinspection PyMethodMayBeStatic
class ActionAbout:
    """
    关于动作类

    该类用于创建一个打开关于页面的动作，该动作可以打开内置关于页面。
    """

    def __init__(self, main_window: QMainWindow):
        """
        初始化动作。

        :param main_window: 所属的主窗口
        :type main_window: QMainWindow
        """
        self.main_window = main_window

        # 关于信息动作
        self.action_about = QAction(QIcon(get_resource_path('media/icons8-about-26.png')), '关于', self.main_window)
        self.action_about.setStatusTip('工具相关信息')
        self.action_about.setShortcut('Shift+F1')
        self.action_about.triggered.connect(self.open_about)

    def open_about(self) -> NoReturn:
        """
        打开关于对话框。

        :rtype: NoReturn
        """
        try:
            dialog = DialogAbout()
            dialog.exec_()
        except Exception as e:
            logger.error(f"An error occurred while opening the about dialog: {e}")
