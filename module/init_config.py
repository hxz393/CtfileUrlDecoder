import logging
import os
from typing import List

from .read_file_to_list import read_file_to_list
from .settings import CONFIG_PATH

logger = logging.getLogger(__name__)


def init_config() -> List[str]:
    """
    从配置文件中初始化并获取用户配置。

    :rtype: List[str]
    :return: 包含 token 和延迟的列表。
    """
    try:
        # 验证配置文件路径是否存在
        if not os.path.exists(CONFIG_PATH):
            logger.error(f"The configuration file '{config_path}' does not exist.")
            return ['0', '0']

        config = read_file_to_list(CONFIG_PATH)

        # 检查配置是否为空，如果为空则提供默认值
        user_token = config[0] if config and len(config) > 0 else '0'
        user_delay = config[1] if config and len(config) > 1 else '0'

        # 检查用户延迟值是否为数字，如果不是，则提供默认值
        user_delay = user_delay if user_delay.isdigit() else '0'

        return [user_token, user_delay]
    except Exception as e:
        logger.error(f"An error occurred while initializing configuration: {e}")
        return ['0', '0']
