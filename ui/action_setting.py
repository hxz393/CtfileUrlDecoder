import logging
from typing import NoReturn

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow

from ui.dialog_settings import DialogSettings
from module.get_resource_path import get_resource_path

logger = logging.getLogger(__name__)


# noinspection PyMethodMayBeStatic
class ActionSetting:
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
