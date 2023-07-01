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
