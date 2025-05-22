# -*- coding:utf-8 -*-
import time
from concurrent.futures import ThreadPoolExecutor

import requests


PROXY_CONFIG = {
    'HOST': '127.0.0.1',
    'PORT': '7890'
}


HTTP_PROXY = {
    'http': '{host}:{port}'.format(host=PROXY_CONFIG['HOST'], port=PROXY_CONFIG['PORT']),
    'https': '{host}:{port}'.format(host=PROXY_CONFIG['HOST'], port=PROXY_CONFIG['PORT'])
}


def _fetch(imei):
    resp = requests.get('https://alpha.imeicheck.com/api/modelBrandName?imei={imei}&format=json'.format(imei=imei), proxies=HTTP_PROXY)
    print(resp.status_code)
    time.sleep(2)
    json_obj = resp.json()
    if len(json_obj) > 2:
        with open(r'C:\Users\Administrator\Desktop\imei_result.text', mode='a', encoding='utf-8') as output:
            output.write('{}|{}|{}\n'.format(imei[:8], json_obj['object']['brand'], ' '.join([json_obj['object']['name'], json_obj['object']['model']])))


if __name__ == '__main__':
    with open(r'C:\Users\Administrator\Desktop\imei.text', encoding='utf-8') as f:
        imeis = f.readlines()

    with ThreadPoolExecutor(1) as pool:
        for imei in imeis:
            for suffix in range(10):
                pool.submit(_fetch, ''.join([imei.strip(), str(suffix)]))
