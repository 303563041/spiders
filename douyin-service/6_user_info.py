from time import time

from config import API_TOKEN
from lib import wrap_api

if __name__ == '__main__':
    device_info = {'device_id': "66762742687",
                   'install_id': "66088143957",
                   'openudid': '3275465180871399',
                   'uuid': '187604370269819'}

    user_id = "110725736365"
    aweme_id = "6615981222587796743"
    time_now = str(int(time()))

    # 获取某人信息
    print(wrap_api("v1/user",
                   {"user_id": user_id},
                   device_info=device_info,
                   token=API_TOKEN
                   ))
