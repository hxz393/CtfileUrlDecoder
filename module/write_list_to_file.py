from pathlib import Path
import logging
from typing import List, Any, Optional, Union

logger = logging.getLogger(__name__)

def write_list_to_file(target_path: Union[str, Path], content: List[Any]) -> Optional[bool]:
    """
    将列表的元素写入文件，每个元素占据文件的一行。

    :param target_path: 文本文件的路径，可以是字符串或 pathlib.Path 对象。
    :type target_path: Union[str, Path]
    :param content: 要写入的列表。
    :type content: List[Any]
    :return: 成功时返回True，失败时返回None。
    :rtype: Optional[bool]
    """
    try:
        target_path = Path(target_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with target_path.open('w', encoding="utf-8") as file:
            file.write("\n".join(str(element) for element in content))
        return True
    except Exception as e:
        logger.error(f"An error occurred while writing to the file at '{target_path}': {e}")
        return None
