"""
这是一个Python文件，其中包含一个函数：filter_correct_link。

函数 filter_correct_link 用于过滤出符合特定正则表达式的链接。这个函数接收一个 link 参数，表示需要过滤的链接，然后用正则表达式进行检查。如果 link 符合给定的正则表达式，则函数会返回这个链接，否则返回 None。在处理过程中如果发生任何异常，函数也会返回 None，并且使用日志记录器 logger 记录错误信息。

这个模块主要用于链接过滤，包括检查链接是否符合特定的正则表达式，以及在需要时返回过滤后的链接。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)


def filter_correct_link(link: str) -> Optional[str]:
    """
    过滤符合指定正则表达式的链接。

    :param link: 待过滤的链接
    :type link: str
    :rtype: Optional[str]
    :return: 符合指定正则表达式的链接，如果不符合则返回 None
    """
    try:
        match_result = re.search(r'^https://.+\.ctfile\.com/f/\d+-\d+-\w+.*', link.strip())
        return match_result.group() if match_result else None
    except Exception as e:
        logger.error(f"An error occurred while filtering links: {e}")
        return None
