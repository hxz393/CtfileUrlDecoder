import logging
from typing import NoReturn

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QAction, QMainWindow

from module.get_resource_path import get_resource_path

logger = logging.getLogger(__name__)


# noinspection PyMethodMayBeStatic
class ActionHelp:
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
