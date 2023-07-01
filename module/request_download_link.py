import logging
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
        logger.error(f"Unable to find link {url}: {e}")
        return '-1'
    except requests.exceptions.RequestException as e:
        logger.error(f"Unable to send network request to {url}: {e}")
        return None
    finally:
        time.sleep(int(delay) / 1000.0)
