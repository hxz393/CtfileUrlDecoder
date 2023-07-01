import logging
from typing import NoReturn

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow

from ui.dialog_about import DialogAbout
from module.get_resource_path import get_resource_path

logger = logging.getLogger(__name__)


# noinspection PyMethodMayBeStatic
class ActionAbout:
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
