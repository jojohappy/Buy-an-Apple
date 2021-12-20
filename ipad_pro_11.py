#!/usr/bin/env python3
#coding=utf-8

from json import JSONDecodeError
import json

import requests

from push import push


def queryQuote():
    cookie = "geo=CN; at_check=true; dssid2=4432c1e9-bd2d-4ce4-acb1-7c86bc1f48ff; dssf=1; as_pcts=ggAXjnfoCvpDPG81ikwTXE7OtCkreasxFVVbP0sB9yyWae4im29GV38DJayGpLbbTM85rtVFHN8pR:P_AiMn9s+gZf-So_40u25V04oYLWWd4:jZq29VCq; as_dc=nc; s_fid=76BE23601108F223-1CEC46617613D3A1; s_cc=true; s_vi=[CS]v1|30E01938BC93F446-60000BA1125D6F19[CE]; as_sfa=Mnxjbnxjbnx8emhfQ058Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE; as_atb=1.0|MjAyMS0xMi0xOSAxMTozNjozMw|89a4f2609f7f4466e967d6ce52d82009fc9497ca; mbox=session#d3151609ca134bf586170647f0eb6395#1639987637|PC#d3151609ca134bf586170647f0eb6395.32_0#1639987595; as_uct=0; as_loc=1f1c3ec76dea21f3e52963c9b2ce0e024f93201825a6cde6860677f2125fd483feb9097cc8c6db539816bafd14d1326735347599b465499638f8ee2a88de6b00c71afe1438bb31f6494c2c45b86b2715b426ec9f32a066b59afa822579082247ea9fbb6a5dddb2cd8f1b2daf9d0a64b12cea1e0c6c2bd8c093daeac76a9bd8d0; rtsid=%7BCN%3D%7Bt%3Da%3Bi%3DR581%3B%7D%3B%7D; s_sq=applestoreww%3D%2526c.%2526a.%2526activitymap.%2526page%253DAOS%25253A%252520home%25252Fshop_ipad%25252Ffamily%25252Fipad_pro%25252Fselect%2526link%253D%252528inner%252520text%252529%252520%25257C%252520no%252520href%252520%25257C%252520body%2526region%253Dbody%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253DAOS%25253A%252520home%25252Fshop_ipad%25252Ffamily%25252Fipad_pro%25252Fselect%2526pidt%253D1%2526oid%253DfunctionVc%252528%252529%25257B%25257D%2526oidt%253D2%2526ot%253DBUTTON"

    headers = {
        'authority': 'www.apple.com.cn',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.apple.com.cn/shop/buy-ipad/ipad-pro/MHQR3CH/A',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': cookie,
    }
    params = {
        'pl': 'true',
        'mt': 'compact',
        'parts.0': 'MHQR3CH/A',
        'location': '\u4E0A\u6D77 \u4E0A\u6D77 \u6D66\u4E1C\u65B0\u533A'
    }

    models = [{
        "key": "MHQR3CH/A",
        "describe": "深空灰色"
    },
    {
        "key": "MHQT3CH/A",
        "describe": "银色"
    }]
    for model in models:
        params['parts.0'] = model["key"]
        response = requests.get('https://www.apple.com.cn/shop/fulfillment-messages', headers=headers, params=params)

        if response.status_code != 200:
            print(f"Query failed: {response.text}")
            push(f"Query failed: {response.text}")

        try:
            response.json()
        except JSONDecodeError as e:
            print(f"JSONDecodeError!!! {e}")
            push(f"JSONDecodeError!!! {e}")

        json_data = response.json()
        stores = json_data["body"]["content"]["pickupMessage"]["stores"]
        print("\n\n\n" + "All stores quote:" + model["describe"])
        for idx, item in enumerate(stores):
            if idx < 7:
                quote = item["partsAvailability"][model["key"]]["pickupSearchQuote"]
                msg = item["storeName"] + ": " + quote
                print(msg)
                if quote != "暂无供应":
                    msg = "GOT ONE!!!\n" + item["storeName"] + ": " + model["describe"] + " " + quote
                    push_telegram(msg)

def push_telegram(text):
    telegram_bot_token = '5046717411:AAH697iEzfZpM__RW0UeZS7p7YMEnxm93vM'
    telegram_chat_id = '1420996115'
    telegram_bot_url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage'
    print(telegram_bot_url)

    data = {
        'chat_id': telegram_chat_id,
        'text': text,
    }
    headers = {'Content-Type': 'application/json'}
    res = requests.post(telegram_bot_url, data=json.dumps(data), headers=headers)
    print(res.json)


if __name__ == '__main__':
    result = queryQuote()
