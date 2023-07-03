"""
这是一个Python文件，包含一个类 `ActionSetting`。

类 `ActionSetting` 用于定义 "设置" 动作。它接受一个参数，`main_window` 代表所属的主窗口。在 `__init__` 方法中，我们定义了一个 QAction 对象 `action_setting`，并将其与 `open_setting` 方法连接。当动作被触发时，`open_setting` 方法会尝试打开设置对话框。

这个模块主要用于定义和实现 "设置" 动作，包括创建动作，设置动作属性和定义动作的触发行为。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import NoReturn

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow

from module.get_resource_path import get_resource_path
from ui.dialog_settings import DialogSettings

logger = logging.getLogger(__name__)


# noinspection PyMethodMayBeStatic
class ActionSetting:
    """
    设置动作类。

    该类用于创建一个打开设置对话框的动作，包括创建动作，设置动作属性和定义动作的触发行为。
    """

    def __init__(self, main_window: QMainWindow):
        """
        初始化动作。

        :param main_window: 所属的主窗口
        :type main_window: QMainWindow
        """
        self.main_window = main_window

        # 设置动作
        self.action_setting = QAction(QIcon(get_resource_path('media/icons8-setting-26.png')), '设置', self.main_window)
        self.action_setting.setStatusTip('打开设置对话框')
        self.action_setting.setShortcut('F11')
        self.action_setting.triggered.connect(self.open_setting)

    def open_setting(self) -> NoReturn:
        """
        打开设置对话框。

        :rtype: NoReturn
        """
        try:
            dialog = DialogSettings()
            dialog.exec_()
        except Exception as e:
            logger.error(f"An error occurred while opening the settings dialog: {e}")
