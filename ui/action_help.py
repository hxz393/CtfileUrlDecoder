"""
这是一个Python文件，其中包含一个类 `ActionHelp`。

类 `ActionHelp` 用于定义 "获取帮助" 动作。它接受一个参数 `main_window`，代表所属的主窗口。在 `__init__` 方法中，我们定义了一个 QAction 对象 `action_help`，并将其与 `open_help_page` 方法连接。当动作被触发时，`open_help_page` 方法会尝试打开在线帮助页面。

这个模块主要用于定义和实现 "获取帮助" 动作，包括创建动作，设置动作属性和定义动作的触发行为。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import NoReturn

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QAction, QMainWindow

from module.get_resource_path import get_resource_path

logger = logging.getLogger(__name__)


# noinspection PyMethodMayBeStatic
class ActionHelp:
    """
    帮助动作类。

    该类用于创建一个获取帮助的动作，该动作可以打开在线帮助页面。
    """

    def __init__(self, main_window: QMainWindow):
        """
        初始化动作。

        :param main_window: 所属的主窗口
        :type main_window: QMainWindow
        """
        self.main_window = main_window

        # 获取帮助动作
        self.action_help = QAction(QIcon(get_resource_path('media/icons8-help-26.png')), '获取帮助', self.main_window)
        self.action_help.setStatusTip('在线获取帮助')
        self.action_help.setShortcut('F1')
        self.action_help.triggered.connect(self.open_help_page)

    def open_help_page(self) -> NoReturn:
        """
        打开在线帮助页面。

        :rtype: NoReturn
        """
        try:
            QDesktopServices.openUrl(QUrl("https://github.com/hxz393/CtfileUrlDecoder"))
        except Exception as e:
            logger.error(f"An error occurred while opening the help page: {e}")
