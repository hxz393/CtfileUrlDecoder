import logging
import sys

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QTextOption, QTextCharFormat, QBrush, QTextCursor
from PyQt5.QtWidgets import (QMainWindow, QAction, QApplication, QLabel, QProgressBar,
                             QSplitter, QVBoxLayout, QWidget, QMessageBox)

from module import *
from ui import *

logger = logging.getLogger(__name__)

logging_config(console_output=True, log_level='INFO')


# noinspection PyMethodMayBeStatic
class Worker(QThread):
    signal = pyqtSignal(str)

    def __init__(self, links, user_token, user_delay):
        super().__init__()
        self.links = links
        self.user_token = user_token
        self.user_delay = user_delay
        self.running = True

    def run(self):
        logger.debug(f'输入列表：{self.links}\n输入令牌：{self.user_token}\n输入延迟：{self.user_delay}')
        try:
            for link in self.links:
                # 中断信号
                if not self.running:
                    break

                self.process_link(link)

        except Exception as e:
            logger.error(e)

    def process_link(self, link):
        link_ok = self.filter_correct_link(link)
        if not link_ok:
            self.signal.emit(f'不支持的链接：{link}')
            return

        file_name, passwd = self.get_file_info(link_ok)

        result = self.request_download_link(file_name, passwd)
        self.handle_download_result(result, link)

    def filter_correct_link(self, link):
        link_ok = filter_correct_link(link)
        logger.debug(f'筛选链接：{link}，结果：{link_ok}')
        return link_ok

    def get_file_info(self, link_ok):
        file_name, passwd = get_file_info(link_ok)
        logger.debug(f'处理链接：{link_ok}，得到文件名：{file_name}，得到密码：{passwd}')
        return file_name, passwd

    def request_download_link(self, file_name, passwd):
        result = request_download_link(file_name, passwd, self.user_token, self.user_delay)
        logger.info(f'请求链接：{file_name}，返回结果：{result}')
        return result

    def handle_download_result(self, result, link):
        if not result:
            self.signal.emit(f'获取下载失败：{link}')
        elif result.startswith("https://"):
            self.signal.emit(result)
        elif result == '-1':
            self.signal.emit(f'没获取到高速链接，请重新登录获取 token：{link}')
        elif result == '401':
            self.signal.emit(f'访问密码缺失或不正确：{link}')
        elif result == '404':
            self.signal.emit(f'文件已删除：{link}')
        elif result == '503':
            self.signal.emit(f'文件已失效：{link}')
        else:
            self.signal.emit(f'错误代码 {result}：{link}')

    def stop(self):
        self.running = False


class CtfileUrlDecoder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 创建文本框
        self.create_text_editor()

        # 创建动作
        self.create_action()

        # 创建菜单栏
        self.create_menubar()

        # 创建工具栏
        self.create_toolbar()

        # 创建状态栏
        self.create_statusbar()

        # 主窗口配置
        self.configure_main_window()

    def create_text_editor(self):
        """
        创建文本框
        """
        # 输入文本框
        self.text_input = CodeEditor()
        self.text_input.setWordWrapMode(QTextOption.NoWrap)
        self.text_input.setStyleSheet("border: none; font-size: 14px;")
        self.text_input.setPlaceholderText("请输入城通链接，格式为：\nhttps://url1.ctfile.com/f/34628125-771711816-13fa54 0000\n或者：\nhttps://url01.ctfile.com/f/13660405-878244288-582bbf?p=AA00AA")

        # 输出文本框
        self.text_output = CodeEditor()
        self.text_output.setWordWrapMode(QTextOption.NoWrap)
        self.text_output.setReadOnly(True)
        self.text_output.setStyleSheet("border: none; font-size: 14px;")
        self.text_output.setPlaceholderText("获取到的会员高速下载地址，可以直接复制粘贴到下载软件批量下载")

        # 使用 QSplitter 将文本框分为左右两栏
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.text_input)
        splitter.addWidget(self.text_output)

        # 创建一个垂直布局，并添加splitter
        main_text_area = QVBoxLayout()
        main_text_area.addWidget(splitter)

        # 获取每个文本框的滚动条并同步
        scrollbar_input = self.text_input.verticalScrollBar()
        scrollbar_output = self.text_output.verticalScrollBar()
        scrollbar_input.valueChanged.connect(scrollbar_output.setValue)
        scrollbar_output.valueChanged.connect(scrollbar_input.setValue)

        # 创建一个 QWidget，将布局应用于此小部件，然后将其设置为主窗口的中心部件
        central_widget = QWidget()
        central_widget.setLayout(main_text_area)
        central_widget.layout().setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(central_widget)

    def create_action(self):
        """
        创建动作
        """
        # 开始动作
        self.action_start = QAction(QIcon(get_resource_path('media/icons8-start-26.png')), '开始', self)
        self.action_start.setShortcut('F10')
        self.action_start.setStatusTip('开始运行')
        self.action_start.triggered.connect(self.start_worker)

        # 停止动作
        self.action_stop = QAction(QIcon(get_resource_path('media/icons8-stop-26.png')), '停止', self)
        self.action_stop.setShortcut('F12')
        self.action_stop.setStatusTip('停止运行')
        self.action_stop.triggered.connect(self.stop_worker)
        self.action_stop.setEnabled(False)

        # 其他动作
        self.ActionOpen = ActionOpen(self, self.text_input)
        self.ActionSave = ActionSave(self, self.text_output)
        self.ActionExit = ActionExit(self)
        self.ActionSetting = ActionSetting(self)
        self.ActionFilter = ActionFilter(self, self.text_output)
        self.ActionHelp = ActionHelp(self)
        self.ActionUpdate = ActionUpdate(self)
        self.ActionAbout = ActionAbout(self)

    def create_menubar(self):
        """
        创建菜单栏
        """
        menubar = self.menuBar()
        menu_file = menubar.addMenu('文件(&F)')
        menu_file.addAction(self.ActionOpen.action_open)
        menu_file.addAction(self.ActionSave.action_save)
        menu_file.addSeparator()
        menu_file.addAction(self.ActionExit.action_exit)
        menu_run = menubar.addMenu('运行(&R)')
        menu_run.addAction(self.action_start)
        menu_run.addAction(self.action_stop)
        menu_option = menubar.addMenu('选项(&O)')
        menu_option.addAction(self.ActionSetting.action_setting)
        menu_option.addAction(self.ActionFilter.action_filter)
        menu_help = menubar.addMenu('帮助(&H)')
        menu_help.addAction(self.ActionHelp.action_help)
        menu_help.addAction(self.ActionUpdate.action_update)
        menu_help.addSeparator()
        menu_help.addAction(self.ActionAbout.action_about)

    def create_toolbar(self):
        """
        创建工具栏
        """
        toolbar = self.addToolBar('工具栏')
        toolbar.addAction(self.ActionOpen.action_open)
        toolbar.addAction(self.ActionSave.action_save)
        toolbar.addSeparator()
        toolbar.addAction(self.action_start)
        toolbar.addAction(self.action_stop)
        toolbar.addSeparator()
        toolbar.addAction(self.ActionSetting.action_setting)
        toolbar.addAction(self.ActionFilter.action_filter)
        toolbar.addSeparator()
        toolbar.addAction(self.ActionAbout.action_about)
        toolbar.addAction(self.ActionExit.action_exit)

    def create_statusbar(self):
        """
        创建状态栏
        """
        self.status_bar = self.statusBar()
        self.progress_label = QLabel('准备就绪：')
        self.status_bar.addPermanentWidget(self.progress_label)
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)

    def configure_main_window(self):
        self.setGeometry(10, 10, 640, 480)
        self.setWindowTitle('CtfileUrlDecoder')
        self.setWindowIcon(QIcon(get_resource_path('media/main.ico')))
        self.show()

        # 移动窗口到屏幕中心
        screenGeometry = QApplication.desktop().screenGeometry()
        x = (screenGeometry.width() - self.width()) / 2
        y = (screenGeometry.height() - self.height()) / 2
        self.move(int(x), int(y))

    def start_worker(self):
        try:
            self.text_output.clear()
            # 初步处理用户输入，删除空行，去重
            processed_text = process_input(self.text_input.toPlainText())
            self.text_input.setPlainText(processed_text)
            if not processed_text:
                self.progress_label.setText(f"准备就绪：")
                self.progress_bar.setValue(0)
                return

            # 获取链接列表、token、延迟参数
            links = processed_text.split("\n")
            user_token, user_delay = init_config()
            if not bool(user_token):
                QMessageBox(QMessageBox.Warning, '检查设置', '请先设置帐号 token！', QMessageBox.Ok, self).show()
                return

            # 丢到子线程运行
            self.worker = Worker(links, user_token, user_delay)
            self.worker.signal.connect(self.update_output)
            self.worker.signal.connect(self.update_progress_bar_and_label)
            self.worker.start()
            self.worker.finished.connect(self.enable_start_button)
            self.worker.finished.connect(self.finalize_output)
            self.disable_start_button()

            self.progress_bar.setMaximum(len(links))
            self.progress_bar.setValue(0)
            self.update_progress_label(0, len(links))

        except Exception as e:
            logger.error(f'运行解析发生错误：{e}')

    def stop_worker(self):
        self.worker.stop()
        self.disable_start_button()

    def update_progress_bar_and_label(self):
        # 每次收到信号，就将进度条的值增加1
        self.progress_bar.setValue(self.progress_bar.value() + 1)
        self.update_progress_label(self.progress_bar.value(), self.progress_bar.maximum())

    def update_progress_label(self, completed, total):
        # 更新标签的文字
        self.progress_label.setText(f"进度：{completed}/{total}")

    def update_output(self, text):
        cursor = self.text_output.textCursor()
        char_format = QTextCharFormat()

        if text.startswith('https://'):
            char_format.setForeground(QBrush(Qt.darkGreen))
        else:
            char_format.setForeground(QBrush(Qt.darkRed))

        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text, char_format)
        cursor.insertText('\n')

        char_format.setForeground(QBrush(Qt.darkGreen))
        cursor.setCharFormat(char_format)

    def finalize_output(self):
        cursor = self.text_output.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.deletePreviousChar()

    def enable_start_button(self):  # 开启按钮
        self.ActionSave.action_save.setEnabled(True)
        self.ActionOpen.action_open.setEnabled(True)
        self.ActionSetting.action_setting.setEnabled(True)
        self.ActionFilter.action_filter.setEnabled(True)
        self.action_start.setEnabled(True)
        self.action_stop.setEnabled(False)

    def disable_start_button(self):  # 关闭按钮
        self.ActionSave.action_save.setEnabled(False)
        self.ActionOpen.action_open.setEnabled(False)
        self.ActionSetting.action_setting.setEnabled(False)
        self.ActionFilter.action_filter.setEnabled(False)
        self.action_start.setEnabled(False)
        self.action_stop.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    _ = CtfileUrlDecoder()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
