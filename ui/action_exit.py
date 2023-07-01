import logging

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow

from module.get_resource_path import get_resource_path

logger = logging.getLogger(__name__)


# noinspection PyMethodMayBeStatic
class ActionExit:
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
