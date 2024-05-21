import sys

sys.path.append(r'd:\program files\workon_home\frida\lib\site-packages')
from io import BytesIO
import pandas as pd

import requests
from urllib.parse import urlencode , unquote_plus
import json
import uuid

import time

import random

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def waitTip(seconds):
    print(f"{timeTo(int(time.time()))}等待剩余时间: {seconds} 秒")
    time.sleep(seconds)
    '''
    for i in range(seconds, 0, -1):
        print(f"等待剩余时间: {i} 秒")
        time.sleep(1)
    '''
    # print("等待结束")


def timeTo(timestamp):
    date_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
    return date_str


def getTipFromCode(code):
    if code == 'Captcha Validate Required':
        return '需要验证码验证  https://buff.163.com/account/m/captcha?origin=selling-list'
    if code == 'Action Forbidden':
        return '市场接口访问功能暂时关闭，请稍后再试'

    return '未知错误码 ' + code


def buyGoods_Confirm(id):
    url = "https://buff.163.com/api/market/manual_plus/buyer_send_offer"

    payload = json.dumps({
        "buff_android_webview_version": "74.0.3729.186",
        "buyer_info": "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",
        "bill_orders": [
            id
        ]
    })

    headers = {
        'User-Agent': "Android/1180/2.82.0.0/b12ab863565f57a0/29/Xiaomi/24030PN60C/aurora/d17101a5-51fb-4d0c-a83e-1706cf86f921",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/json",
        'app-version': "1180",
        'app-version-code': "2.82.0.0",
        'brand': "xiaomi",
        'build-fingerprint': "xiaomi/aurora/aurora:10/UKQ1.230804.001/eng.build.20231013.013027:user/release-keys",
        'channel': "Official",
        'device-id': "d17101a5-51fb-4d0c-a83e-1706cf86f921",
        'device-id-weak': "b12ab863565f57a0",
        'manufacturer': "Xiaomi",
        'model': "24030PN60C",
        'network': "WIFI/",
        'product': "aurora",
        'resolution': "1080x2256",
        'rom': "UKQ1.230804.001 release-keys",
        'rom-id': "UKQ1.230804.001",
        'screen-density': "480.00",
        'screen-size': "6.19",
        'seed': "3625a6d814360d765d9dd5d7f36ad660",
        'sign': "Hello, world!",
        'system-type': "Android",
        'system-version': "29",
        'timestamp': "1710924285.261",
        'timezone': "China Standard Time",
        'timezone-offset': "28800000",
        'timezone-offset-dst': "28800000",
        'locale': "zh_CN",
        'locale-supported': "zh-Hans",
        'devicename': "RMX3161",
        'Cookie': "session=1-fDaxB6uVJeOw8sjRp5h6rTJmXe1saOhfD7H3AWDHzXEn2031187764"
    }

    response = requests.post(url, data=payload, headers=headers, verify=False)
    while True:
        if response.status_code != 200:
            print('创建报价失败:', response.status_code)
            break

        print('创建报价结果: ')
        print(response.text.encode('utf-8').decode('unicode-escape'))
        break


def buyGoods(sell_order_id, price):
    url = "https://buff.163.com/api/market/goods/buy"

    payload = json.dumps({
        "batch_buy": 0,
        "game": "csgo",
        "sell_order_id": sell_order_id,
        "price": price,
        "pay_method": "3",
        "allow_tradable_cooldown": "1"
    })

    headers = {
        'User-Agent': "Android/1180/2.82.0.0/b12ab863565f57a0/29/Xiaomi/24030PN60C/aurora/d17101a5-51fb-4d0c-a83e-1706cf86f921",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/json",
        'app-version': "1180",
        'app-version-code': "2.82.0.0",
        'brand': "xiaomi",
        'build-fingerprint': "xiaomi/aurora/aurora:10/UKQ1.230804.001/eng.build.20231013.013027:user/release-keys",
        'channel': "Official",
        'device-id': "d17101a5-51fb-4d0c-a83e-1706cf86f921",
        'device-id-weak': "b12ab863565f57a0",
        'manufacturer': "Xiaomi",
        'model': "24030PN60C",
        'network': "WIFI/",
        'product': "aurora",
        'resolution': "1080x2256",
        'rom': "UKQ1.230804.001 release-keys",
        'rom-id': "UKQ1.230804.001",
        'screen-density': "480.00",
        'screen-size': "6.19",
        'seed': "85074695d4f8d8940306734fb336a9b2",
        'sign': "Hello, world!",
        'system-type': "Android",
        'system-version': "29",
        'timestamp': "1710927457.412",
        'timezone': "China Standard Time",
        'timezone-offset': "28800000",
        'timezone-offset-dst': "28800000",
        'locale': "zh_CN",
        'locale-supported': "zh-Hans",
        'devicename': "RMX3161",
        'Cookie': "session=1-fDaxB6uVJeOw8sjRp5h6rTJmXe1saOhfD7H3AWDHzXEn2031187764"
    }

    response = requests.post(url, data=payload, headers=headers, verify=False)

    while True:

        if response.status_code != 200:
            print('购买请求失败:', response.status_code)
            break
        print('购买结果: ')
        print(response.text.encode('utf-8').decode('unicode-escape'))
        response_json = json.loads(response.text)
        data = response_json.get('data')
        if data is None:
            print('response_json: 不存在data成员')
            break

        id = data.get('id')
        if id is None:
            print('data: 不存在id成员')
            break

        print('交易单号: ', id)
        time.sleep(3)
        buyGoods_Confirm(id)
        break


def generate_random_hex_string(length):
    hex_chars = '0123456789abcdef'
    return ''.join(random.choice(hex_chars) for _ in range(length))


def randomDeviceId():
    return str(uuid.uuid4())


def get_good_detail(classid, assetid):
    url = f"https://buff.163.com/api/market/item_detail?game=csgo&classid={classid}&assetid={assetid}"

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41",
        'sec-ch-ua': "\"Microsoft Edge\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        'x-requested-with': "XMLHttpRequest",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://buff.163.com/goods/769177",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        'Cookie': ''
    }

    response = requests.get(url, headers=headers, verify=False)

    price_total = 0.0
    while True:
        if response.status_code != 200:
            print('get_good_detail请求失败:', response.status_code)
            break
        response_json = json.loads(response.text)
        data_json = response_json.get('data')
        if data_json is None:
            print('get_good_detail失败:')
            break

        asset_info_json = data_json.get('asset_info')
        if asset_info_json is None:
            print('get_good_detail失败:')
            break
        stickers_json = asset_info_json.get('stickers')
        if stickers_json is None:
            print('get_good_detail失败:')
            break

        for index, item in enumerate(stickers_json):
            sell_reference_price = float(item['sell_reference_price'])
            price_total += sell_reference_price
        break

    return price_total


def add_bookmark(id):
    url = "https://buff.163.com/account/api/add_bookmark/batch"

    payload = json.dumps({
        "target_type": 3,
        "target_ids": str(id)
    })

    headers = {
        'User-Agent': "Android/1180/2.82.0.0/b12ab863565f57a0/29/Xiaomi/24030PN60C/aurora/629b2e6c-1471-4818-ae2a-fbf6f08797e7",
        'brand': "xiaomi",
        'channel': "Official",
        'manufacturer': "Xiaomi",
        'network': "NONE",
        'product': "aurora",
        'resolution': "1080x2256",
        'rom': "UKQ1.230804.001 release-keys",
        'rom-id': "UKQ1.230804.001",
        'screen-density': "480.00",
        'screen-size': "6.19",
        'sign': "Hello, world!",
        'system-type': "Android",
        'system-version': "29",
        'locale': "zh_CN",
        'locale-supported': "zh-Hans",
        'devicename': "RMX3161",
        'content-type': "application/json; charset=utf-8",
        'accept-encoding': "gzip",
        'Cookie': "session=1-fDaxB6uVJeOw8sjRp5h6rTJmXe1saOhfD7H3AWDHzXEn2031187764"
    }

    response = requests.put(url, data=payload, headers=headers, verify=False)

    while True:
        if response.status_code != 200:
            print('收藏饰品请求失败:', response.status_code)
            break
        response_json = json.loads(response.text)
        if response_json['code'] != 'OK':
            print("收藏饰品失败")
            print(response.text)
            break
        print("收藏饰品成功")
        break


def goods_monitor(goods_id):
    url = "https://buff.163.com/api/market/goods/info?goods_id=" + str(goods_id)

    headers = {
        'User-Agent': "",
        'Accept-Encoding': "gzip",
        'app-version': "1180",
        'app-version-code': "2.82.0.0",
        'brand': "",
        'build-fingerprint': "",
        'channel': "Official",
        'device-id': randomDeviceId(),
        'device-id-weak': generate_random_hex_string(16),
        'manufacturer': "",
        'model': "",
        'network': "NONE",
        'product': "",
        'resolution': "1080x2256",
        'rom': "",
        'rom-id': "",
        'screen-density': "480.00",
        'screen-size': "6.19",
        'seed': generate_random_hex_string(32),
        'sign': "Hello, world!",
        'system-type': "Android",
        'system-version': "29",
        'timestamp': str(round(time.time(), 3)),
        'timezone': "China Standard Time",
        'timezone-offset': "28800000",
        'timezone-offset-dst': "28800000",
        'locale': "zh_CN",
        'locale-supported': "zh-Hans",
        'devicename': "",
        'Cookie': "session="
    }

    res = {
        'sell_num': 0,
        'sell_min_price': 0.0
    }
    response = requests.get(url, headers=headers, verify=False)
    while True:
        if response.status_code != 200:
            print('监视请求失败:', response.status_code)
            break
        response_json = json.loads(response.text)

        data = response_json.get('data')
        if data is None:
            print('response_json:没有data成员')
            break

        sell_min_price = data.get('sell_min_price')
        if sell_min_price is None:
            print('data:没有sell_min_price成员')
            break

        sell_num = data.get('sell_num')
        if sell_num is None:
            print('data:没有sell_num成员')
            break
        # print(sell_num)
        res['sell_num'] = int(sell_num)
        res['sell_min_price'] = float(sell_min_price)
        break
    return res


def searchForGoods(searchArgs, price_buy, cookie):
    url = "https://buff.163.com/api/market/goods/sell_order?" + urlencode(searchArgs)

    '''
    cookie = '1-2nP1oBKHEmmtLIcs3Gl4fxSBlhytsamb4gHadG_cGBdi2027763368'
    cookie = '1-bK2vmn2tJf1lHW9TYjCRHZG7Kc9IttfEYCFTHwsqnMl12027763368'
    '''
    headers = {
        'User-Agent': "",
        'Accept-Encoding': "gzip",
        'app-version': "1180",
        'app-version-code': "2.82.0.0",
        'brand': "xiaomi",
        'build-fingerprint': "",
        'channel': "Official",
        'device-id': randomDeviceId(),
        'device-id-weak': generate_random_hex_string(16),
        'manufacturer': "Xiaomi",
        'model': "",
        'network': "WIFI/",
        'product': "aurora",
        'resolution': "1080x2256",
        'rom': "",
        'rom-id': "",
        'screen-density': "480.00",
        'screen-size': "6.19",
        'seed': generate_random_hex_string(32),
        'sign': "Hello, world!",
        'system-type': "Android",
        'system-version': "29",
        'timestamp': str(round(time.time(), 3)),
        'timezone': "China Standard Time",
        'timezone-offset': "28800000",
        'timezone-offset-dst': "28800000",
        'locale': "zh_CN",
        'locale-supported': "zh-Hans",
        'devicename': "",
        'Cookie': "session=" + cookie
    }

    response = requests.get(url, headers=headers, verify=False)

    while True:
        if response.status_code != 200:
            print('搜索请求失败:', response.status_code)
            break
        # print('请求成功:', response.text.encode('utf-8').decode('unicode-escape'))

        response_json = json.loads(response.text)
        if response_json['code'] != 'OK':
            print(getTipFromCode(response_json['code']))
            break

        data = response_json.get('data')
        if data is None:
            print('response_json: 不存在data成员')
            break

        goods_infos = data.get('goods_infos')
        if goods_infos is None:
            print('response_json: 不存在goods_infos成员')
            break

        goodName = goods_infos.get(searchArgs['goods_id'])
        if goodName is None:
            print('goods_infos: 不存在 ' + searchArgs['goods_id'] + ' 成员中的goodName1')
            break

        goodName = goodName.get('name')
        if goodName is None:
            print('goods_infos: 不存在 ' + searchArgs['goods_id'] + ' 成员中的goodName2')
            break

        items = data.get('items')
        if items is None:
            print('data: 不存在items成员')
            break

        if len(items) == 0:
            print('items成员数量为0')
            break
        for i,vv in enumerate(items):
            price = vv.get('price')
            if price is None:
                print('items: 不存在price成员')
                break

            id = vv.get('id')
            if id is None:
                print('items: 不存在id成员')
                break
            timestamp = int(time.time() * 1000)
            print(goodName + '  ' + timeTo(timestamp / 1000) + '  价格:' + price)
            if float(price) <= price_buy:
                print('-----------购买-------------')
                buyGoods(id, price)
                time.sleep(10)

        # print(items[0]['id'])
        break


def searchForGoods_sp(searchArgs, cookie):
    price_lowst = goods_monitor(searchArgs['goods_id'])['sell_min_price']
    url = "https://buff.163.com/api/market/goods/sell_order?" + urlencode(
        searchArgs) + f'&max_price={int(price_lowst * 3.0)}'

    '''
    cookie = '1-2nP1oBKHEmmtLIcs3Gl4fxSBlhytsamb4gHadG_cGBdi2027763368'
    cookie = '1-bK2vmn2tJf1lHW9TYjCRHZG7Kc9IttfEYCFTHwsqnMl12027763368'
    '''

    headers = {
        'User-Agent': "",
        'Accept-Encoding': "gzip",
        'app-version': "1180",
        'app-version-code': "2.82.0.0",
        'brand': "xiaomi",
        'build-fingerprint': "",
        'channel': "Official",
        'device-id': randomDeviceId(),
        'device-id-weak': generate_random_hex_string(16),
        'manufacturer': "Xiaomi",
        'model': "",
        'network': "WIFI/",
        'product': "aurora",
        'resolution': "1080x2256",
        'rom': "",
        'rom-id': "",
        'screen-density': "480.00",
        'screen-size': "6.19",
        'seed': generate_random_hex_string(32),
        'sign': "Hello, world!",
        'system-type': "Android",
        'system-version': "29",
        'timestamp': str(round(time.time(), 3)),
        'timezone': "China Standard Time",
        'timezone-offset': "28800000",
        'timezone-offset-dst': "28800000",
        'locale': "zh_CN",
        'locale-supported': "zh-Hans",
        'devicename': "",
        'Cookie': "session=" + cookie
    }

    response = requests.get(url, headers=headers, verify=False)

    while True:
        if response.status_code != 200:
            print('搜索请求失败:', response.status_code)
            break
        # print('请求成功:', response.text.encode('utf-8').decode('unicode-escape'))

        response_json = json.loads(response.text)
        if response_json['code'] != 'OK':
            print(getTipFromCode(response_json['code']))
            break

        data = response_json.get('data')
        if data is None:
            print('response_json: 不存在data成员')
            break

        goods_infos = data.get('goods_infos')
        if goods_infos is None:
            print('response_json: 不存在goods_infos成员')
            break

        goodName = goods_infos.get(searchArgs['goods_id'])
        if goodName is None:
            print('goods_infos: 不存在 ' + searchArgs['goods_id'] + ' 成员中的goodName1')
            break

        goodName = goodName.get('name')
        if goodName is None:
            print('goods_infos: 不存在 ' + searchArgs['goods_id'] + ' 成员中的goodName2')
            break

        items = data.get('items')
        if items is None:
            print('data: 不存在items成员')
            break

        if len(items) == 0:
            print('items成员数量为0')
            break

        for index, item in enumerate(items):
            sticker_premium = item.get('sticker_premium')
            if sticker_premium is None:
                print('item: 不存在sticker_premium成员')
                break
            if sticker_premium * 100.0 > 5.0:
                break

            asset_info = item.get('asset_info')
            if asset_info is None:
                print('item: 不存在asset_info成员')
                break

            assetid = asset_info.get('assetid')
            if assetid is None:
                print('asset_info: 不存在assetid成员')
                break

            classid = asset_info.get('classid')
            if classid is None:
                print('asset_info: 不存在classid成员')
                break
            sticker_price_total = get_good_detail(classid, assetid)
            price = item.get('price')
            if price is None:
                print('item: 不存在price成员')
                break

            updated_at = item.get('updated_at')
            if updated_at is None:
                print('item: 不存在updated_at成员')
                break
            created_at = item.get('created_at')
            if created_at is None:
                print('item: 不存在created_at成员')
                break

            goods_id = item.get('goods_id')
            if goods_id is None:
                print('item: 不存在goods_id成员')
                break

            id = item.get('id')
            if id is None:
                print('item: 不存在id成员')
                break

            can_make_money = (6.0 - sticker_premium * 100.0) / 100.0 * sticker_price_total
            can_make_money = can_make_money - (float(price) + can_make_money) * 0.025
            price_add = sticker_price_total * sticker_premium

            print(
                f'{goodName}  上架时间:{timeTo(created_at)}  更新时间:{timeTo(updated_at)}  价格:{float(price):<10.1f}  印花总价:{sticker_price_total:<10.1f}  sp:{round(sticker_premium * 100.0, 2)}%   底价:{price_lowst:<10.1f}   可赚:{can_make_money:<10.1f}')

            if (can_make_money < 5.0):
                continue

            print('------------------------------------------------------')
            add_bookmark(id)
            print('------------------------------------------------------')
        # print(items[0]['id'])
        break


# buyGoods_Confirm('240320T0949217946')
# buyGoods('0842226398-7285-137413048','0.02')


def getGoodsInfo():
    url = "https://docs.qq.com/v1/export/export_office"

    payload = "exportType=0&switches=%7B%22embedFonts%22%3Afalse%7D&exportSource=client&docId=300000000%24BffEnzCanNLb&version=2"

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41",
        'Accept': "application/json, text/plain, */*",
        'Content-Type': "application/x-www-form-urlencoded",
        'sec-ch-ua': "\"Microsoft Edge\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        'traceparent': "00-a4991ede134952844bfb83de5dcf7e9e-e37d510491d48466-01",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'origin': "https://docs.qq.com",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://docs.qq.com/sheet/DQmZmRW56Q2FuTkxi?tab=BB08J2",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        'Cookie': "uid=144115210433732257; uid_key=EOP1mMQHGixSWXYrU3FFc0dmNitYVU44YmFCenJMek10T0FaRDBreGNyRkI0WDhlR09zPSKBAmV5SmhiR2NpT2lKQlEwTkJURWNpTENKMGVYQWlPaUpLVjFRaWZRLmV5SlVhVzU1U1VRaU9pSXhORFF4TVRVeU1UQTBNek0zTXpJeU5UY2lMQ0pXWlhJaU9pSXhJaXdpUkc5dFlXbHVJam9pYzJGaGMxOTBiMk1pTENKU1ppSTZJbFp1ZVVwdGR5SXNJbVY0Y0NJNk1UY3hOalF5TnpRNE5pd2lhV0YwSWpveE56RXpPRE0xTkRnMkxDSnBjM01pT2lKVVpXNWpaVzUwSUVSdlkzTWlmUS5jdXZiTUVCemhiaVZrLU1MZHV2YjloYm4zUkNmd2psRmdfUnAzck9wVms0KN61urIGMAE%3D"
    }

    response = requests.post(url, data=payload, headers=headers, verify=False)
    if response.status_code != 200:
        print('获取商品腾讯文档operationId失败')
        return
    response_json = json.loads(response.text)
    operationId = response_json['operationId']
    print(operationId)
    time.sleep(0.5)

    url = "https://docs.qq.com/v1/export/query_progress?operationId=" + operationId

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41",
        'Accept': "application/json, text/plain, */*",
        'sec-ch-ua': "\"Microsoft Edge\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        'traceparent': "00-01a10351584f615fd881700c3a013f25-d5ec5e23cbc2793f-01",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://docs.qq.com/sheet/DQmhTQ1RPYVdtaW9X?tab=BB08J2",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        'Cookie': "uid=144115210433732257; uid_key=EOP1mMQHGixSWXYrU3FFc0dmNitYVU44YmFCenJMek10T0FaRDBreGNyRkI0WDhlR09zPSKBAmV5SmhiR2NpT2lKQlEwTkJURWNpTENKMGVYQWlPaUpLVjFRaWZRLmV5SlVhVzU1U1VRaU9pSXhORFF4TVRVeU1UQTBNek0zTXpJeU5UY2lMQ0pXWlhJaU9pSXhJaXdpUkc5dFlXbHVJam9pYzJGaGMxOTBiMk1pTENKU1ppSTZJbFp1ZVVwdGR5SXNJbVY0Y0NJNk1UY3hOalF5TnpRNE5pd2lhV0YwSWpveE56RXpPRE0xTkRnMkxDSnBjM01pT2lKVVpXNWpaVzUwSUVSdlkzTWlmUS5jdXZiTUVCemhiaVZrLU1MZHV2YjloYm4zUkNmd2psRmdfUnAzck9wVms0KN61urIGMAE%3D"
    }

    response = requests.get(url, headers=headers, verify=False)
    if response.status_code != 200:
        print('根据operationId获取下载地址失败')
        return
    response_json = json.loads(response.text)
    file_url = response_json.get('file_url')
    print(file_url)

    url = file_url

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        'sec-ch-ua': "\"Microsoft Edge\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'Upgrade-Insecure-Requests': "1",
        'Sec-Fetch-Site': "cross-site",
        'Sec-Fetch-Mode': "navigate",
        'Sec-Fetch-User': "?1",
        'Sec-Fetch-Dest': "document",
        'Referer': "https://docs.qq.com/",
        'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
    }

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code != 200:
        print('下载文档失败')
        return

    return response.content




search_argAry = []
search_argAry_sp = []
search_cookies = []

excel_byte = getGoodsInfo()

# 读取整个 Excel 文件
excel_data = pd.read_excel(BytesIO(excel_byte), sheet_name='goods_b')  # 如果有多个工作表，可以指定sheet_name
excel_data2 = pd.read_excel(BytesIO(excel_byte), sheet_name='cookies')  # 如果有多个工作表，可以指定sheet_name
excel_data3 = pd.read_excel(BytesIO(excel_byte), sheet_name='goods_sp')  # 如果有多个工作表，可以指定sheet_name


# 查看读取的数据
for index, row in excel_data.iterrows():
    json_data = json.loads(row.to_json())

    search_arg = {
        'id': {
            'buff': str(json_data['buff']),
            'youyou': str(json_data['youyou']),
            'skinport': str(json_data['skinport']),
            'igxe': str(json_data['igxe']),

        },
        '最低磨损': str(json_data['最低磨损']),
        '最高磨损': str(json_data['最高磨损']),
        '购入价格': str(json_data['购入价格']),
    }
    search_argAry.append(search_arg)

    print(json.dumps(json_data).encode('utf8').decode('unicode_escape'))

    continue



# 查看读取的数据
for index, row in excel_data3.iterrows():
    json_data = json.loads(row.to_json())
    search_arg_sp = {
        'id': {'buff': json_data['buff'],
               'youyou': json_data['youyou'],
               'skinport': json_data['skinport'],
               'igxe': json_data['igxe']}

    }
    search_argAry_sp.append(search_arg_sp)
    print(json.dumps(json_data).encode('utf8').decode('unicode_escape'))

# 查看读取的数据
for index, row in excel_data2.iterrows():
    json_data = json.loads(row.to_json())
    cookie = {
        'buff': json_data['buff'],
        'youyou': json_data['youyou'],
        'skinport': json_data['skinport'],
        'igxe': json_data['igxe']
    }
    search_cookies.append(cookie)
    print(f'第{index + 1}个cookie: ' + str(cookie))

'''
while True:
    sell_nums = []
    buy_prices = []
    searchs = []
    print('初始化商品信息...')
    for index, search_arg in enumerate(search_argAry_sp):
        searchArgs = {
            'goods_id': str(search_arg['id']['buff']),
            'page_num': '1',
            'page_size': '100',
            'allow_tradable_cooldown': '1',
            'sort_by': 'sticker_premium.asc',
            # 'min_price': '0',
            # 'max_price': '10',
            'game': 'csgo'

        }

        searchs.append(searchArgs)

    start_time = int(time.time())
    print("开始时间: " + timeTo(start_time))
    while True:
        for cookie in search_cookies:
            print(f'开始搜索 cookic: {cookie['buff']}')
            for index, searchArgs in enumerate(searchs):
                # print(searchArgs, buy_prices[index], cookie)
                searchForGoods_sp(searchArgs, cookie['buff'])
                waitTip(random.randint(8, 12))
            waitTip(random.randint(30 * 60, 45 * 60))
        end_time = int(time.time())
        if end_time > start_time + 60 * 60:
            print('结束时间: ' + timeTo(end_time))
            break

    # waitTip(random.randint(60 * 60, 70 * 60))
    break
'''
while True:
    sell_nums = []
    buy_prices = []
    searchs = []
    print('初始化商品信息...')
    for index, search_arg in enumerate(search_argAry):
        searchArgs = {
            'goods_id': str(search_arg['id']['buff']),
            'page_num': '1',
            'page_size': '100',
            'allow_tradable_cooldown': '1',
            'check_reduction': 'false',
            'sort_by': 'price.asc',
            'min_paintwear': str(search_arg['最低磨损']),
            'max_paintwear': str(search_arg['最高磨损']),
            # 'min_price': '0',
            # 'max_price': '10',
            'game': 'csgo',
            'appid': '730'
        }

        searchs.append(searchArgs)
        buy_prices.append(float(search_arg['购入价格']))
        sell_nums.append(int(goods_monitor(search_arg['id']['buff'])['sell_num']))
        time.sleep(0.1)

    start_time = int(time.time())
    print("开始时间: " + timeTo(start_time))
    while True:
        for cookie in search_cookies:
            print(f'开始搜索 cookic: {cookie['buff']}')
            for index, searchArgs in enumerate(searchs):
                sell_num = goods_monitor(searchArgs['goods_id'])['sell_num']

                if sell_nums[index] == sell_num:
                    time.sleep(0.1)
                    continue
                if sell_nums[index] > sell_num:
                    sell_nums[index] = sell_num
                    time.sleep(0.1)
                    continue

                print('有商品上架: ' + str(sell_nums[index]) + " to " + str(sell_num))
                sell_nums[index] = sell_num
                # print(searchArgs, buy_prices[index], cookie)
                searchForGoods(searchArgs, buy_prices[index], cookie['buff'])
                waitTip(random.randint(3, 5))
            waitTip(random.randint(2 * 60, 3 * 60))
        end_time = int(time.time())
        if end_time > start_time + 60 * 60:
            print('结束时间: ' + timeTo(end_time))
            break

    # waitTip(random.randint(60 * 60, 70 * 60))
    break
