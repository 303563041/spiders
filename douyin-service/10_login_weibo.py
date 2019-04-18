from time import time

import requests

from config import API_TOKEN
from lib import wrap_api, sign


def weibo_login(device_info, access_token, uid):
    # cURL
    # GET https://is.snssdk.com/passport/auth/login/

    params = {
        "platform": "sina_weibo",
        "access_token": access_token,
        "expires_in": str(int(time())),
        "uid": uid,
        "retry_type": "no_retry",
        "iid": device_info['install_id'],
        "device_id": device_info['device_id'],
        "ac": "wifi",
        "channel": "wandoujia_zhiwei",
        "aid": "1128",
        "app_name": "aweme",
        "version_code": "290",
        "version_name": "2.9.0",
        "device_platform": "android",
        "ssmix": "a",
        "device_type": "ONEPLUS A6010",
        "device_brand": "OnePlus",
        "language": "zh",
        "os_api": "28",
        "os_version": "9",
        "uuid": device_info['uuid'],
        "openudid": device_info['openudid'],
        "manifest_version_code": "290",
        "resolution": "1080*2261",
        "dpi": "420",
        "update_version_code": "2902",
        "_rticket": str(int(time())) + "000",
    }
    args = ""
    for (idx, val) in params.items():
        args += "&{0}={1}".format(idx, val)
    original_url = "http://is.snssdk.com/passport/auth/login/?" + args

    signed_url = sign(original_url, token=API_TOKEN)
    print(signed_url)
    response = requests.get(
        url=signed_url,
        headers={
            "Cache-Control": "max-stale=0",
            "Sdk-Version": "1",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.10.0.1",
        },
    )
    print('Response HTTP Status Code: {status_code}'.format(
        status_code=response.status_code))
    print('Response HTTP Response Body: {content}'.format(
        content=response.content.decode("utf-8")))
    print('Response HTTP Response Cookie: {cookie}'.format(
        cookie=response.cookies.items()))


if __name__ == '__main__':
    device_info = {'device_id': "66954874663,",
                   'install_id': "67439526519",
                   'openudid': '0952463183701895',
                   'uuid': '980576262409148'}

    # 获取首页feed
    weibo_login(device_info, "2.00tqDDPHGahxaB1c41db103aUXCJuD", "6635304659")
