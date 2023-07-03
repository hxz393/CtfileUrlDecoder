"""
这是一个Python文件，其中包含一个函数：init_config。

函数 init_config 用于初始化并获取用户配置，这些配置存储在预定义的配置文件中。函数首先验证配置文件路径是否存在，如果不存在，则记录错误信息并返回默认的配置列表。如果配置文件存在，函数将调用 read_file_to_list 函数读取配置文件的内容，并从中获取 user_token 和 user_delay 两个配置项。如果配置项不存在或格式不正确，函数将为它们提供默认值。如果所有操作都成功，函数将返回一个包含 user_token 和 user_delay 的列表。如果在处理过程中发生任何错误，函数将记录错误信息并返回默认的配置列表。

这个模块主要用于初始化和获取用户配置，包括用户的令牌和延迟配置。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

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
            logger.error(f"The configuration file '{CONFIG_PATH}' does not exist.")
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
