"""
这是一个Python文件，包含了两个类：`UpdateChecker` 和 `ActionUpdate`。

`UpdateChecker` 是一个QThread线程类，用于在线检查更新。该类首先在初始化时定义了一个PyQt信号`signal`，然后在`run`方法中尝试获取最新版本的信息并通过该信号发送出去。如果在获取过程中发生异常，它会捕获该异常并记录在日志中，然后通过信号发送None。

`ActionUpdate` 类用于定义 "检查更新" 动作。它接受一个参数，`main_window` 代表所属的主窗口。在 `__init__` 方法中，我们定义了一个 QAction 对象 `action_update`，并将其与 `check_update` 方法连接。当动作被触发时，`check_update` 方法会尝试检查更新，并根据检查结果显示相应的提示信息。

这个模块主要用于定义和实现 "检查更新" 动作，包括创建动作，设置动作属性，定义动作的触发行为，以及在线获取最新版本信息。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import NoReturn

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow, QMessageBox

from module.get_resource_path import get_resource_path
from module.request_url import request_url
from module.settings import VERSION_INFO, CHECK_UPDATE_URL

logger = logging.getLogger(__name__)


class UpdateChecker(QThread):
    """
    更新检查线程类。

    该类在单独的线程中执行更新检查，并通过 PyQt 信号机制将最新的版本信息或错误通知发出。
    """

    signal = pyqtSignal(str)

    def __init__(self):
        """
        初始化更新检查线程。

        """
        super().__init__()

    def run(self) -> NoReturn:
        """
        线程运行函数。

        :rtype: NoReturn
        """
        try:
            latest_version = request_url(CHECK_UPDATE_URL)
            self.signal.emit(latest_version)
        except Exception as e:
            logger.error(f"An error occurred while checking for updates: {e}")
            self.signal.emit(None)


class ActionUpdate:
    """
    检查更新动作类。

    该类用于创建一个检查更新的动作，包括创建动作，设置动作属性，定义动作的触发行为，以及处理动作的结果。
    """

    def __init__(self, main_window: QMainWindow):
        """
        初始化动作。

        :param main_window: 所属的主窗口
        :type main_window: QMainWindow
        """
        self.main_window = main_window

        # 检查更新动作
        self.action_update = QAction(QIcon(get_resource_path('media/icons8-update-26.png')), '检查更新', self.main_window)
        self.action_update.setStatusTip('在线检查更新')
        self.action_update.setShortcut('F2')
        self.action_update.triggered.connect(self.check_update)

    def check_update(self) -> NoReturn:
        """
        检查更新。

        :rtype: NoReturn
        """
        self.action_update.setEnabled(False)
        self.update_checker = UpdateChecker()
        self.update_checker.signal.connect(self.show_update_message)
        self.update_checker.start()

    def show_update_message(self, latest_version: str) -> NoReturn:
        """
        显示更新消息。

        :param latest_version: 最新的版本号
        :type latest_version: str
        :rtype: NoReturn
        """
        self.action_update.setEnabled(True)
        current_version = VERSION_INFO

        if bool(latest_version) is False:
            QMessageBox(QMessageBox.Warning, '检查更新', '检查更新失败！', QMessageBox.Ok, self.main_window).show()
        elif latest_version != current_version:
            QMessageBox(QMessageBox.Information, '检查更新', f'有新版发布\n\n当前版本：{current_version}\n最新版本：{latest_version}', QMessageBox.Ok, self.main_window).show()
        elif latest_version == current_version:
            QMessageBox(QMessageBox.Information, '检查更新', f'不需要更新\n\n最新版本：{current_version}', QMessageBox.Ok, self.main_window).show()
