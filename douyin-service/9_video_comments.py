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

    # 获取某个视频的评论列表
    print(wrap_api("v1/comment/list",
                   {"aweme_id": aweme_id, "cursor": 0, "count": 20},
                   device_info=device_info,
                   token=API_TOKEN
                   ))
