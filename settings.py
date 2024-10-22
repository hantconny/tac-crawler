# -*- coding:utf-8 -*-
import os.path
import time

"""
命名规则为/home/rhino/{project}/{sub-proj}
project可选值为: ip, sns, tor, tac
sub-proj可选值为: 
  ip: v4, v6
  sns: tt, ins, fb, tw, ut
  tor: 直接存放
  tac: 直接存放
"""
DUMP_DIR = '/home/rhino/tac'
if not os.path.exists(DUMP_DIR):
    os.makedirs(DUMP_DIR)

# 20231202
TODAY = time.strftime('%Y%m%d', time.localtime())
CHROME_TEST = 'D:/ENV/chromedriver/chrome-win64/chrome.exe'

PROXY_ENABLED = False
HTTP_PROXY = '127.0.0.1:7890'

RETRY_LIMIT = 5