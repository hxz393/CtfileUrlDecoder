"""
这是一个Python文件，包含一个类 `ActionOpen`。

类 `ActionOpen` 用于定义 "打开文件" 动作。它接受两个参数，`main_window` 代表所属的主窗口，`text_input` 是链接文本框。在 `__init__` 方法中，我们定义了一个 QAction 对象 `action_open`，并将其与 `open_file` 方法连接。当动作被触发时，`open_file` 方法会尝试打开一个文件并将其内容读取到链接文本框。

这个模块主要用于定义和实现 "打开文件" 动作，包括创建动作，设置动作属性和定义动作的触发行为。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import os
from typing import Optional

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QFileDialog, QMainWindow

from module import MAX_FILE_SIZE
from module.get_resource_path import get_resource_path
from ui.code_editor import CodeEditor

logger = logging.getLogger(__name__)


class ActionOpen:
    """
    打开文件类。

    该类用于创建一个打开文件的动作，该动作可以打开一个文件并将其内容读取到链接文本框。
    """

    def __init__(self, main_window: QMainWindow, text_input: CodeEditor):
        """
        初始化动作。

        :param main_window: 所属的主窗口
        :type main_window: QMainWindow
        :param text_input: 链接文本框
        :type text_input: CodeEditor
        """
        self.main_window = main_window
        self.text_input = text_input

        self.action_open = QAction(QIcon(get_resource_path('media/icons8-open-26.png')), '打开', self.main_window)
        self.action_open.setShortcut('Ctrl+O')
        self.action_open.setStatusTip('打开链接文本文件')
        self.action_open.triggered.connect(self.open_file)

    def open_file(self) -> Optional[str]:
        """
        打开文件并将其内容读取到链接文本框。

        :rtype: Optional[str]
        :return: 如果操作成功则返回打开的文件的路径，如果操作失败则返回 None
        """
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self.main_window, "打开文件", "", "文本文件 (*.txt);;所有类型 (*)", options=options)
        if file_name:
            if os.path.getsize(file_name) > MAX_FILE_SIZE:
                logger.error(f'The file is too large to open: {file_name}')
                return None

            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    self.text_input.setPlainText(file.read())
                    return file_name
            except IOError:
                logger.error(f'Unable to open file: {file_name}')
            except UnicodeDecodeError:
                logger.error(f'Unable to read file: {file_name}')

        return None
