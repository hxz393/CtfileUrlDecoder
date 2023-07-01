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
        passwd = re.sub(r'[^\x00-\x7F]+', '', passwd) # 删除所有非 ASCII 编码字符
        passwd = passwd.strip()
        return file_name, passwd
    except Exception as e:
        logger.error(f"An error occurred while retrieving file information: {e}")
        return None
