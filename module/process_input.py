"""
这是一个Python文件，其中包含一个函数：process_input。

函数 process_input 用于处理用户输入的字符串。它接受一个参数 input_str，这是需要处理的字符串。函数首先将 input_str 分割成多行，然后移除所有的空行和重复行。为了做到这一点，函数创建了一个名为 seen 的集合，用来跟踪已经见过的行。然后，函数通过列表解析来移除空行和已经见过的行。最后，函数将剩下的行重新组合成一个字符串，并返回这个字符串。如果在处理过程中发生任何错误，函数将记录错误信息并返回 None。

这个模块主要用于处理用户输入，包括去除空行和重复行。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


def process_input(input_str: str) -> Optional[str]:
    """
    处理用户输入，去除空行和重复行后返回。

    :param input_str: 待处理的用户输入字符串
    :type input_str: str
    :rtype: Optional[str]
    :return: 去除空行和重复行后的字符串，或者在发生错误时返回 None。
    """
    try:
        # 分割成行
        lines = input_str.split("\n")

        # 移除空行和重复行
        seen = set()
        lines = [line for line in lines if line.strip() != "" and not (line in seen or seen.add(line))]

        # 将剩下的行重新组合成一个字符串
        output_str = "\n".join(lines)

        return output_str
    except Exception as e:
        logger.error(f"An error occurred while processing the input: {e}")
        return None
