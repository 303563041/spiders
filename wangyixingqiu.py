#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from elasticsearch import Elasticsearch, helpers
import requests
import time
import sys

# 领取黑钻的请求


def getCollectCoins(serialNumber):
    cookies = {
        'mp_MA-9E66-C87EFACB60BC_hubble': '%7B%22sessionReferrer%22%3A%20%22%22%2C%22updatedTime%22%3A%201541746563337%2C%22sessionStartTime%22%3A%201541745948401%2C%22deviceUdid%22%3A%20%220c7f13cc-7f12-45ba-9b9e-ede9e3fd900f%22%2C%22persistedTime%22%3A%201541739058922%2C%22LASTEVENT%22%3A%20%7B%22eventId%22%3A%20%22click%22%2C%22time%22%3A%201541746563338%7D%2C%22sessionUuid%22%3A%20%22221d5557-e041-4d8e-a9de-91de73ecd490%22%2C%22user_id%22%3A%208411%7D',
        'NTES_YD_SESS': '0EGImViy23cumCi0_CCtBJilfTKwp0RJydNlrHu0ZlciO1zGOBYERDROXhx1kfqrmuutfY8.NiEinNXJ8SAUI8.3MBeF1v5jTxcmK2AO4FPGxYaUEUhDhtAvZB2dpzT19GbaFW..wrY9Jt_ZbQpbFeqVLc8Ajrd.GN1FxhpOrPGcJURG9YZPWYNR4eesz6hvnHt0toQBOeYcR7oE2sIivDdhtea5rcxrvYRred4NSIgik',
        'STAR_YD_SESS': '0EGImViy23cumCi0_CCtBJilfTKwp0RJydNlrHu0ZlciO1zGOBYERDROXhx1kfqrmuutfY8.NiEinNXJ8SAUI8.3MBeF1v5jTxcmK2AO4FPGxYaUEUhDhtAvZB2dpzT19GbaFW..wrY9Jt_ZbQpbFeqVLc8Ajrd.GN1FxhpOrPGcJURG9YZPWYNR4eesz6hvnHt0toQBOeYcR7oE2sIivDdhtea5rcxrvYRred4NSIgik',
        'STAREIG': '7a8529f981ec6f63d7200c44248a8bcb511b59f4',
    }

    headers = {
        'Host': 'star.8.163.com',
        'Accept': 'application/json, text/plain, */*',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'en-us',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://star.8.163.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; COL-AL10 Build/HUAWEICOL-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 hybrid/1.0.0 star_client_info_begin {hybridVersion: "1.0.0",clientVersion: "1.7.4",accountId: "ccc9f06797c104c669784081574441742aea8feedd5a06ba37cf3c67def41702",channel: "e01170007"}star_client_info_end',
        'Referer': 'https://star.8.163.com/m',
    }
    data = '{"serialNumber": \"%s\"}' % serialNumber
    response = requests.post('https://star.8.163.com/api/starUserCoin/collectUserCoin',
                             headers=headers, cookies=cookies, data=data)

    # print response.json()

def es(datas, index="xingqiu", type="xingqiu"):
    """
    insert es
    """
    es = Elasticsearch([{"host": "localhost", "port": 9200}])
    actions = [
        {
            '_op_type': 'index',
            '_index': index,
            '_type': type,
            '_source': d
        }
        for d in datas
    ]

    try:
        helpers.bulk( es, actions )
    except Exception, e:
        print e
        sys.exit(1)

def main():
    updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    cookies = {
        'mp_MA-9E66-C87EFACB60BC_hubble': '%7B%22sessionReferrer%22%3A%20%22%22%2C%22updatedTime%22%3A%201541746563337%2C%22sessionStartTime%22%3A%201541745948401%2C%22deviceUdid%22%3A%20%220c7f13cc-7f12-45ba-9b9e-ede9e3fd900f%22%2C%22persistedTime%22%3A%201541739058922%2C%22LASTEVENT%22%3A%20%7B%22eventId%22%3A%20%22click%22%2C%22time%22%3A%201541746563338%7D%2C%22sessionUuid%22%3A%20%22221d5557-e041-4d8e-a9de-91de73ecd490%22%2C%22user_id%22%3A%208411%7D',
        'NTES_YD_SESS': '0EGImViy23cumCi0_CCtBJilfTKwp0RJydNlrHu0ZlciO1zGOBYERDROXhx1kfqrmuutfY8.NiEinNXJ8SAUI8.3MBeF1v5jTxcmK2AO4FPGxYaUEUhDhtAvZB2dpzT19GbaFW..wrY9Jt_ZbQpbFeqVLc8Ajrd.GN1FxhpOrPGcJURG9YZPWYNR4eesz6hvnHt0toQBOeYcR7oE2sIivDdhtea5rcxrvYRred4NSIgik',
        'STAR_YD_SESS': '0EGImViy23cumCi0_CCtBJilfTKwp0RJydNlrHu0ZlciO1zGOBYERDROXhx1kfqrmuutfY8.NiEinNXJ8SAUI8.3MBeF1v5jTxcmK2AO4FPGxYaUEUhDhtAvZB2dpzT19GbaFW..wrY9Jt_ZbQpbFeqVLc8Ajrd.GN1FxhpOrPGcJURG9YZPWYNR4eesz6hvnHt0toQBOeYcR7oE2sIivDdhtea5rcxrvYRred4NSIgik',
        'STAREIG': '7a8529f981ec6f63d7200c44248a8bcb511b59f4',
    }

    headers = {
        'Host': 'star.8.163.com',
        'Accept': 'application/json, text/plain, */*',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'en-us',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://star.8.163.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; COL-AL10 Build/HUAWEICOL-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 hybrid/1.0.0 star_client_info_begin {hybridVersion: "1.0.0",clientVersion: "1.7.4",accountId: "ccc9f06797c104c669784081574441742aea8feedd5a06ba37cf3c67def41702",channel: "e01170007"}star_client_info_end',
        'Referer': 'https://star.8.163.com/m',
    }

    data = '{"type":0}'

    try:
        # 获取黑钻的请求
        response = requests.post('https://star.8.163.com/api/home/v2/userInfoAndCollectCoins',
                                 headers=headers, cookies=cookies, data=data)
        collectCoins = response.json()['data']['collectCoins']

        if len(collectCoins) == 0:
            print "[ {0} ] {1}".format(updatetime, 0)
        else:
            coins = 0
            for collectCoinsItem in collectCoins:
                getCollectCoins(collectCoinsItem['serialNumber'])
                coins = coins + float(collectCoinsItem['virCount'])

    except Exception as e:
        coins = -1

    datas = [
                {
                    "num": coins,
                    "@timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000", time.localtime())
                }
            ]
    es(datas)
    
    print "[ {0} ] {1}".format(updatetime, value)


if __name__ == "__main__":
    main()
