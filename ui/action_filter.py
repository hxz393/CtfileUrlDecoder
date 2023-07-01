import logging
from typing import NoReturn

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QTextCharFormat, QBrush
from PyQt5.QtWidgets import QAction, QMainWindow

from ui.code_editor import CodeEditor
from module.get_resource_path import get_resource_path

logger = logging.getLogger(__name__)


class ActionFilter:
    def __init__(self, main_window: QMainWindow, text_output: CodeEditor):
        """
        初始化动作。

        :param main_window: 所属的主窗口
        :type main_window: QMainWindow
        :param text_output: 输出文本框
        :type text_output: CodeEditor
        """
        self.main_window = main_window
        self.text_output = text_output

        # 过滤动作
        self.action_filter = QAction(QIcon(get_resource_path('media/icons8-filter-26.png')), '过滤', self.main_window)
        self.action_filter.setStatusTip('过滤掉失败链接')
        self.action_filter.setShortcut('F7')
        self.action_filter.triggered.connect(self.filter_output)

    def filter_output(self) -> NoReturn:
        """
        过滤输出信息。

        :rtype: NoReturn
        """
        try:
            filtered_text = '\n'.join(line for line in self.text_output.toPlainText().split('\n') if line.startswith('https://'))
            default_format = QTextCharFormat()
            default_format.setForeground(QBrush(Qt.darkGreen))
            self.text_output.setCurrentCharFormat(default_format)
            self.text_output.setPlainText(filtered_text)
        except Exception as e:
            logger.error(f"An error occurred while filtering output: {e}")
