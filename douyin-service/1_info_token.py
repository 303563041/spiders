from config import ROUTE_INFO_TOKEN, API_TOKEN
from lib import api_service

def get_token_info():
    try:
        data = api_service(route=ROUTE_INFO_TOKEN, method="get", token=API_TOKEN)
        return data
    except Exception as e:
        print("error", e)

if __name__ == '__main__':
    print(get_token_info()['info']['times'])
