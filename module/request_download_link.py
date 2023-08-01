"""
这是一个Python文件，其中包含一个函数：`request_download_link`。

函数 `request_download_link` 用于向城通服务器请求下载链接。它接受四个参数，分别是需要下载的文件名 `file`，访问密码 `passwd`，用户token `token` 以及请求之间的延迟时间 `delay`。首先，函数构建了一个URL，包含了这四个参数以及一个随机数。然后，它发送了一个GET请求到这个URL，并把响应解析为JSON。如果响应的代码是200，函数返回下载链接，否则返回错误代码。在发生错误时，如找不到链接或网络请求失败，函数将返回相应的错误信息或 `None`。无论是否成功，函数在最后都会根据 `delay` 参数进行暂停。

此模块主要用于与城通服务器进行交互，包括请求下载链接并处理可能的错误。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import traceback
import random
import time
from typing import Optional

import requests
from retrying import retry

from .settings import REQUEST_HEAD

requests.packages.urllib3.disable_warnings()
logger = logging.getLogger(__name__)


@retry(stop_max_attempt_number=5, wait_random_min=100, wait_random_max=1200)
def request_download_link(file: str, passwd: str, token: str, delay: str) -> Optional[str]:
    """
    向城通服务器请求下载链接。

    :type file: str
    :param file: 需要下载的文件名
    :type passwd: str
    :param passwd: 访问密码
    :type token: str
    :param token: 用户 token
    :type delay: str
    :param delay: 请求之间的延迟，单位是毫秒
    :rtype: Optional[str]
    :return: 服务器返回的下载链接，或者在发生错误时返回 None
    """
    url = f'https://webapi.ctfile.com/getfile.php?path=f&f={file}&passcode={passwd}&token={token}&r={str(random.random())}&ref='
    try:
        response = requests.get(url=url, headers=REQUEST_HEAD, timeout=15, verify=False, allow_redirects=True)
        response.raise_for_status()

        response_json = response.json()
        logger.debug(f'response_json: {response_json}')
        response_json_code = response_json['code']

        if response_json_code == 200:
            download_link = response_json['file']['vip_dx_url']
            return download_link
        else:
            return str(response_json_code)
    except (KeyError, ValueError) as e:
        logger.error(f"Unable to find link {url}: {e}\n{traceback.format_exc()}")
        return '-1'
    finally:
        time.sleep(int(delay) / 1000.0)
