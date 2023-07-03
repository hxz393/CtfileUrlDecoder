"""
这是一个Python文件，其中包含一个类 `ActionFilter`。

类 `ActionFilter` 用于定义 "过滤" 动作。它接受两个参数 `main_window` 和 `text_output`，分别代表所属的主窗口和输出文本框。在 `__init__` 方法中，我们定义了一个 QAction 对象 `action_filter`，并将其与 `filter_output` 方法连接。当动作被触发时，`filter_output` 方法会尝试过滤掉输出信息中不以 'https://' 开头的行。

这个模块主要用于定义和实现 "过滤" 动作，包括创建动作，设置动作属性和定义动作的触发行为。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import NoReturn

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QTextCharFormat, QBrush
from PyQt5.QtWidgets import QAction, QMainWindow

from module.get_resource_path import get_resource_path
from ui.code_editor import CodeEditor

logger = logging.getLogger(__name__)


class ActionFilter:
    """
    过滤动作类。

    该类用于创建一个过滤动作，该动作可以过滤输出信息中不以 'https://' 开头的行。
    """

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
