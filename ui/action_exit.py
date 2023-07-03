"""
这是一个Python文件，其中包含一个类 `ActionExit`。

类 `ActionExit` 用于定义 "退出" 动作。它接受一个参数 `main_window`，这是所属的主窗口。在 `__init__` 方法中，我们定义了一个 QAction 对象 `action_exit`，并将其与 `exit` 方法连接。当动作被触发时，`exit` 方法会尝试退出应用程序。

这个模块主要用于定义和实现 "退出" 动作，包括创建动作，设置动作属性和定义动作的触发行为。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow

from module.get_resource_path import get_resource_path

logger = logging.getLogger(__name__)


# noinspection PyMethodMayBeStatic
class ActionExit:
    """
    退出动作类

    该类用于创建一个退出程序的动作，该动作可以安全地退出程序。
    """

    def __init__(self, main_window: QMainWindow):
        """
        初始化退出动作。

        :param main_window: 主窗口的实例
        :type main_window: QMainWindow
        """
        self.main_window = main_window

        self.action_exit = QAction(QIcon(get_resource_path('media/icons8-exit-26.png')), '退出', self.main_window)
        self.action_exit.setShortcut('Ctrl+Q')
        self.action_exit.setStatusTip('退出程序')
        self.action_exit.triggered.connect(self.exit)

    def exit(self):
        """
        关闭程序。

        :rtype: None
        """
        try:
            QCoreApplication.quit()
        except Exception as e:
            logger.error(f"An error occurred while exiting the application: {e}")
