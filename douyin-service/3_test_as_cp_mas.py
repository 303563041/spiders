from config import API_TOKEN
from lib import sign


def test_sign(token):
    print(sign(
        "https://api-hl.amemv.com/aweme/v1/commit/follow/user/?user_id=60514131756&type=1&retry_type=no_retry&iid=65734914098&device_id=66679620049&ac=wifi&channel=wandoujia_zhiwei&aid=1128&app_name=aweme&version_code=290&version_name=2.9.0&device_platform=android&ssmix=a&device_type=ONEPLUS%20A6010&device_brand=OnePlus&language=zh&os_api=28&os_version=9&uuid=432635101856947&openudid=8522097096784651&manifest_version_code=290&resolution=1080*2261&dpi=420&update_version_code=2902&_rticket=1552285914901",
        token=token))


if __name__ == '__main__':
    device_info = {'device_id': "67199318829",
                   'install_id': "69045087173",
                   'openudid': '8074983237510961',
                   'uuid': '047510716293536'}

    # 测试签名
    test_sign(API_TOKEN)
