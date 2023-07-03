"""
这是一个Python文件，包含两个类：`LineNumberArea` 和 `CodeEditor`。

`LineNumberArea` 是一个自定义的QWidget，用于显示行号。这个类与一个QPlainTextEdit实例（在这里是我们的代码编辑器）相关联，并将其作为一个参数传递给构造函数。它还定义了一个`paintEvent`方法，该方法在需要更新行号显示区域的内容时调用。

`CodeEditor` 是一个继承自QPlainTextEdit的类，用于创建一个具有行号显示功能的代码编辑器。它包含一系列方法，用于计算行号区域的宽度，更新行号区域的大小和内容，以及在代码编辑器的大小改变时重新设置行号区域的几何形状。

这个模块主要用于在Qt应用程序中创建一个代码编辑器，该代码编辑器具有行号显示功能。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QSizePolicy, QPlainTextEdit

logger = logging.getLogger(__name__)


class LineNumberArea(QWidget):
    """
    行号显示区域类。

    这个类继承自QWidget，用于创建一个用于显示行号的区域。
    """

    def __init__(self, editor: QPlainTextEdit):
        """
        :param editor: 代码编辑器实例。
        :type editor: QPlainTextEdit
        """
        super().__init__(editor)
        self.my_editor = editor

    def sizeHint(self):
        """
        提示行号显示区域的理想大小。
        :return: 尺寸策略，表示理想的宽度和高度。
        :rtype: QSizePolicy
        """
        return QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

    def paintEvent(self, event):
        """
        重绘行号显示区域。
        :param event: 重绘事件。
        """
        self.my_editor.lineNumberAreaPaintEvent(event)


class CodeEditor(QPlainTextEdit):
    """
    代码编辑器类。

    这个类继承自QPlainTextEdit，用于创建一个具有行号显示功能的代码编辑器。
    """

    def __init__(self, parent=None):
        """
        :param parent: 父控件，默认为None。
        """
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth(0)

    def lineNumberAreaWidth(self) -> int:
        """
        计算行号显示区域的宽度。
        :return: 行号显示区域的宽度。
        :rtype: int
        """
        digits = len(str(max(1, self.blockCount())))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        """
        更新代码编辑器的视口边距以适应行号显示区域。
        """
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        """
        在代码编辑器的文本块（行）更新时，更新行号显示区域。
        :param rect: 需要更新的文本块的矩形区域。
        :param dy: 垂直滚动距离。
        """
        self.lineNumberArea.scroll(0, dy) if dy else self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        """
        重设代码编辑器的大小时，重设行号显示区域的几何形状。
        :param event: 大小改变事件。
        """
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        """
        绘制行号。
        :param event: 绘制事件。
        """
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor(240, 240, 240))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, round(top), self.lineNumberArea.width(), self.fontMetrics().height(), Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1
