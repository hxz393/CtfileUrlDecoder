import re
import logging
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
