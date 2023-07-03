"""
这是一个Python文件，其中包含一个函数：get_file_info。

函数 get_file_info 用于从给定的链接中获取文件名和密码。该函数接受一个字符串参数 link，这是需要处理的链接。函数首先通过正则表达式和字符串替换操作，从链接中分割出文件名和密码。然后，它使用另一个正则表达式删除密码中的所有非ASCII字符，并对结果进行清洗。如果所有操作都成功，函数将返回一个包含文件名和密码的元组。如果在处理过程中发生任何错误，函数将返回 None，并使用日志记录器 logger 记录错误信息。

这个模块主要用于处理链接，从中提取文件信息，包括文件名和密码。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import re
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


def get_file_info(link: str) -> Optional[Tuple[str, str]]:
    """
    从链接分割所需文件信息。

    :param link: 待处理的链接
    :type link: str
    :rtype: Optional[Tuple[str, str]]
    :return: 分割出来的文件名和密码，或者在发生错误时返回 None。
    """
    try:
        name_pass = re.sub(r'.*/f/', '', link)
        name_pass_new = name_pass.replace('?p=', ' ') + ' '
        file_name, passwd = name_pass_new.split(' ', maxsplit=1)
        passwd = re.sub(r'[^\x00-\x7F]+', '', passwd)  # 删除所有非 ASCII 编码字符
        passwd = passwd.strip()
        return file_name, passwd
    except Exception as e:
        logger.error(f"An error occurred while retrieving file information: {e}")
        return None
