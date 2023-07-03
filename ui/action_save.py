"""
这是一个Python文件，包含一个类 `ActionSave`。

类 `ActionSave` 用于定义 "保存文件" 动作。它接受两个参数，`main_window` 代表所属的主窗口，`text_output` 是输出文本框。在 `__init__` 方法中，我们定义了一个 QAction 对象 `action_save`，并将其与 `save_file` 方法连接。当动作被触发时，`save_file` 方法会尝试保存文件并将输出文本框中的内容写入到文件。

这个模块主要用于定义和实现 "保存文件" 动作，包括创建动作，设置动作属性和定义动作的触发行为。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Optional

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QFileDialog, QMainWindow

from module.get_resource_path import get_resource_path
from ui.code_editor import CodeEditor

logger = logging.getLogger(__name__)


class ActionSave:
    """
    保存文件类。

    该类用于创建一个保存文件的动作，该动作可以将输出文本框中的内容写入到文件。
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

        self.action_save = QAction(QIcon(get_resource_path('media/icons8-save-26.png')), '保存', self.main_window)
        self.action_save.setShortcut('Ctrl+S')
        self.action_save.setStatusTip('保存解析结果到文件')
        self.action_save.triggered.connect(self.save_file)

    def save_file(self) -> Optional[str]:
        """
        保存文件并将输出文本框中的内容写入到文件。

        :rtype: Optional[str]
        :return: 如果操作成功则返回保存的文件的路径，如果操作失败则返回 None
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self.main_window, "保存到文件", "", "文本文件 (*.txt);;所有类型 (*)",
                                                   options=options)
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(self.text_output.toPlainText())
                    return file_name
            except IOError:
                logger.error(f'Unable to save to file: {file_name}')
        return None
