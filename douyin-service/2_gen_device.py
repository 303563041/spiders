import base64
import json
import random
from time import time

import requests

from config import API_TOKEN, ROUTE_CRYPT_DOUYIN
from lib import api_service


def get_new_device_info(token):
    client_uuid = "".join(random.sample("01234567890123456789", 15))
    serial_number = "".join(random.sample("0123456789" + "abcdef", 16))
    openudid = "".join(random.sample("01234567890123456789", 16))
    params = {}
    data = {"time_sync": {"local_time": str(int(time())), "server_time": str(int(time()))},
            "magic_tag": "ss_app_log",
            "header": {"sdk_version": 1132, "language": "zh",
                       "user_agent": "okhttp/2.9.0",
                       "app_name": "aweme", "app_version": "2.9.0", "is_upgrade_user": 0, "region": "CN",
                       "vendor_id": serial_number, "app_region": "CN",
                       "channel": "App Store", "mcc_mnc": "46001",
                       "custom": {"app_region": "CN", "build_number": "29001", "app_language": "zh"},
                       "resolution": "1125*2436", "aid": "1128", "os": "Android", "tz_offset": 28800,
                       "access": "WIFI", "openudid": openudid,
                       "carrier": "%D6%D0%B9%FA%D2%C6%B6%AF", "is_jailbroken": 0, "os_version": "11.4",
                       "app_language": "zh", "device_model": "OnePlus",
                       "display_name": "%B6%B6%D2%F4%B6%CC%CA%D3%C6%B5", "mc": "02:00:00:00:00:00",
                       "package": "com.ss.android.ugc.Aweme", "timezone": 8, "tz_name": "Asia\/Shanghai",
                       "idfa": client_uuid}, "fingerprint": ""}

    try:
        data = api_service(route=ROUTE_CRYPT_DOUYIN, token=token, method="post", data=json.dumps(data),
                           content_type="application/json")
        data = base64.b64decode(data['base64_data'])
        headers = {
            'Content-Type': 'application/octet-stream;tt-data=a',
            'sdk-version': '1',
            'user-agent': 'okhttp/3.10.0.1',
        }
        resp = requests.post("http://log.snssdk.com/service/2/device_register/", params=params, headers=headers,
                             data=data)
        content = resp.content.decode("utf-8")
        new_device = json.loads(content)
        new_device['openudid'] = openudid
        new_device['android_id'] = serial_number
        new_device['uuid'] = client_uuid
        new_device['iid'] = new_device['install_id']

        return new_device
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    device_info = get_new_device_info(API_TOKEN)
    print(device_info)
