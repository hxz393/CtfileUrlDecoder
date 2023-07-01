import logging
from typing import Optional

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QFileDialog, QMainWindow

from ui.code_editor import CodeEditor
from module.get_resource_path import get_resource_path

logger = logging.getLogger(__name__)


class ActionSave:
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
