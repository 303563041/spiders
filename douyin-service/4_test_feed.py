#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import API_TOKEN
from lib import wrap_api
import requests
import subprocess

def upload_youbube(title, video):
  stdout, stderr = subprocess.Popen('/usr/local/var/pyenv/shims/youtube-upload --title={0} --privacy=private {1}'.format(title, video), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  if stderr.


if __name__ == '__main__':
    device_info = {'device_id': "67199318829",
                   'install_id': "69045087173",
                   'openudid': '8074983237510961',
                   'uuid': '047510716293536'}
    videos_path = "./videos/"

    # 获取首页feed
    videos = wrap_api("v1/feed",
                   {'count': 6, 'type': 0, 'max_cursor': 0, 'min_cursor': -1, 'pull_type': 2},
                   device_info=device_info,
                   token=API_TOKEN)

    for i in videos['aweme_list']:
        title = i['share_info']['share_title']
        download_url = i['video']['play_addr']['url_list'][0]
        r = requests.get(download_url)

        try:
            with open(videos_path + title + '.mp4', 'wb') as f:
                f.write(r.content)
            f.close()
            print('<< {0} >> 下载成功'.format(title))
        except Exception as e:
            print('<< {0} >> 下载失败，Expection: {1}'.format(title, e))
            continue
