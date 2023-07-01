import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QFormLayout, QTextEdit

from module.settings import VERSION_INFO
from module.get_resource_path import get_resource_path

logger = logging.getLogger(__name__)


# noinspection PyMethodMayBeStatic
class DialogAbout(QDialog):
    def __init__(self):
        super(DialogAbout, self).__init__(flags=Qt.Dialog | Qt.WindowCloseButtonHint)

        self.setWindowTitle("关于")
        self.setFixedSize(403, 470)
        self.setWindowIcon(QIcon(get_resource_path('media/icons8-about-26.png')))
        self.setStyleSheet("font-size: 14px;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        try:
            self.construct_first_group(layout)
            self.construct_second_group(layout)
            self.construct_third_group(layout)
        except Exception as e:
            logger.error(f"An error occurred while constructing AboutDialog: {e}")

        self.setLayout(layout)

    def construct_first_group(self, layout: QVBoxLayout):
        """
        构建第一组部件，包括图标。

        :param layout: 主布局
        :type layout: QVBoxLayout
        """
        first_group_layout = QHBoxLayout()
        first_group_layout.setContentsMargins(0, 0, 0, 0)
        first_group_widget = QWidget()
        first_group_widget.setStyleSheet("background-color: white;")
        first_group_widget.setLayout(first_group_layout)

        ## 图标
        image = QLabel()
        image.setContentsMargins(20, 10, 20, 10)
        image.setPixmap(QPixmap(get_resource_path("media/main-96.ico")))
        first_group_layout.addWidget(image)

        title_and_version_layout = QVBoxLayout()
        self.add_title_and_version(title_and_version_layout)

        first_group_layout.addLayout(title_and_version_layout)
        first_group_layout.addStretch()

        layout.addWidget(first_group_widget)

    def add_title_and_version(self, layout: QVBoxLayout):
        """
        添加标题和版本信息部件。

        :param layout: 主布局
        :type layout: QVBoxLayout
        """
        title = QLabel("CtfileUrlDecoder")
        title.setContentsMargins(0, 10, 20, 0)
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(title)

        name = QLabel("城通网盘批量解析工具")
        name.setContentsMargins(0, 20, 0, 0)
        layout.addWidget(name)

        version = QLabel(f"版本: {VERSION_INFO}")
        version.setContentsMargins(0, 0, 0, 10)
        layout.addWidget(version)

    def construct_second_group(self, layout: QVBoxLayout):
        """
        构建第二组部件，包括作者、网站和项目主页信息。

        :param layout: 主布局
        :type layout: QVBoxLayout
        """
        second_group_layout = QFormLayout()
        second_group_layout.setContentsMargins(20, 10, 20, 10)
        second_group_layout.setSpacing(10)

        self.add_author_info(second_group_layout)
        self.add_website_info(second_group_layout)
        self.add_project_info(second_group_layout)

        layout.addLayout(second_group_layout)

    def add_author_info(self, layout: QFormLayout):
        """
        添加作者信息部件。

        :param layout: 主布局
        :type layout: QFormLayout
        """
        author_label = QLabel("作者：")
        author_label.setStyleSheet("font-weight: bold;")
        author_info = QLabel("<a href='https://github.com/hxz393'>assassing</a>")
        author_info.setTextFormat(Qt.RichText)
        author_info.setTextInteractionFlags(Qt.TextBrowserInteraction)
        author_info.setOpenExternalLinks(True)
        layout.addRow(author_label, author_info)

    def add_website_info(self, layout: QFormLayout):
        """
        添加网站信息部件。

        :param layout: 主布局
        :type layout: QFormLayout
        """
        website_label = QLabel("网站：")
        website_label.setStyleSheet("font-weight: bold;")
        website_info = QLabel("<a href='https://blog.x2b.net'>https://blog.x2b.net</a>")
        website_info.setTextFormat(Qt.RichText)
        website_info.setTextInteractionFlags(Qt.TextBrowserInteraction)
        website_info.setOpenExternalLinks(True)
        layout.addRow(website_label, website_info)

    def add_project_info(self, layout: QFormLayout):
        """
        添加项目主页信息部件。

        :param layout: 主布局
        :type layout: QFormLayout
        """
        project_label = QLabel("主页：")
        project_label.setStyleSheet("font-weight: bold;")
        project_info = QLabel("<a href='https://github.com/hxz393/CtfileUrlDecoder'>https://github.com/hxz393/CtfileUrlDecoder</a>")
        project_info.setTextFormat(Qt.RichText)
        project_info.setTextInteractionFlags(Qt.TextBrowserInteraction)
        project_info.setOpenExternalLinks(True)
        layout.addRow(project_label, project_info)

    def construct_third_group(self, layout: QVBoxLayout):
        """
        构建第三组部件，包括程序简介和使用限制。

        :param layout: 主布局
        :type layout: QVBoxLayout
        """
        info_label = QLabel("说明：")
        info_label.setStyleSheet("font-weight: bold;")
        info_label.setContentsMargins(20, 0, 0, 0)

        layout.addWidget(info_label)

        info = QTextEdit()
        info.setHtml(self.get_info_text())
        info.setReadOnly(True)

        layout.addWidget(info)

    def get_info_text(self) -> str:
        """
        返回信息文本。

        :rtype: str
        :return: 信息文本
        """
        # 使用信息
        info_text = """
        <p style="text-align: center; font-size: 16px; font-weight: bold;">程序简介</p>
        <p style="text-align: justify;">
        &nbsp;&nbsp;这是一个批量解析城通网盘下载地址的工具。通过批量解析出直连下载地址，省去在浏览器访问、输入提取码、点击下载的重复步骤，节约人力时间。<br>
        </p>

        <p style="text-align: center; font-size: 16px; font-weight: bold;">获取帮助</p>
        <p style="text-align: justify;">
        &nbsp;&nbsp;请查阅项目主页或网站中的使用说明，如有问题和建议请到项目主页提交 issue。<br>
        </p>

        <p style="text-align: center; font-size: 16px; font-weight: bold;">使用限制</p>
        <p style="text-align: justify;">
        &nbsp;&nbsp;1.必须要有城通会员。非会员只能单任务下载，且下载速度限制在 80KB/s，解析出来也没意义。<br>
        &nbsp;&nbsp;2.只支持单文件链接类型。例如：https://url99.ctfile.com/f/13660000-723149000-b1800a?p=1230。旧城通网盘链接支持有限，文件夹链接可到页面获取批量下载地址。<br>
        &nbsp;&nbsp;3.城通有请求速度限制。持续解析 400 条以上，会出现解析失败，需要等 2~5 分钟方可继续。可以设置请求间隔时间，来保持长时间作业。<br>
        &nbsp;&nbsp;4.下载地址有时效。解析出来的下载地址有效时间为 12 个小时。<br>
        </p>

        <p style="text-align: center; font-size: 16px; font-weight: bold;">构建工具</p>
        <p style="text-align: justify;">
        &nbsp;&nbsp;CtfileUrlDecoder 的构建用到以下工具：
        </p>
        <p><b>&nbsp;&nbsp;程序：</b>Python 3.10.4</p>
        <p><b>&nbsp;&nbsp;界面：</b>PyQT 5.15.8</p>
        <p><b>&nbsp;&nbsp;图标：</b><a href='https://icons8.com/'>icons8.com</a></p>
        """
        return info_text
