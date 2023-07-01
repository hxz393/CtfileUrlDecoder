import logging
from typing import NoReturn

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow, QMessageBox

from module.request_url import request_url
from module.settings import VERSION_INFO, CHECK_UPDATE_URL
from module.get_resource_path import get_resource_path

logger = logging.getLogger(__name__)


class UpdateChecker(QThread):
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
