# -*- coding:utf-8 -*-
import time
from concurrent.futures import ThreadPoolExecutor
from io import StringIO

import cloudscraper
import pandas
from DrissionPage._pages.chromium_page import ChromiumPage
from loguru import logger
from lxml import etree

from CloudflareBypasser import CloudflareBypasser
from settings import *

logger.add(os.path.join(DUMP_DIR, 'tac_crawler_{time:YYYYMMDD}.log'), rotation="50 MB", retention="3 days",
           compression="gz", enqueue=True)


def _fetch(_page, driver):
    driver.get('https://swappa.com/imei/tac?page={}'.format(_page))

    tables = pandas.read_html(StringIO(driver.html), converters={'TAC': str, 'Devices': str, 'Brand': str})

    with open(os.path.join(DUMP_DIR, 'tac_{ts}.text'.format(ts=TODAY)), mode='a', encoding='utf-8') as f:
        for table in tables:
            for line in zip(table['TAC'], table['Brand'], table['Devices']):
                tac, brand, devices = line
                # logger.debug(line)
                """
                页面devices为空的项在解析后会变成float类型的nan，对于此类型的数据，直接转成空字符串
                """
                f.write('|'.join([tac, brand, '' if type(devices) is float else devices]) + '\n')

    logger.success('page {} done', _page)

    time.sleep(10)


if __name__ == '__main__':

    driver = ChromiumPage()
    driver.get('https://swappa.com/imei/tac')

    cf_bypasser = CloudflareBypasser(driver)
    cf_bypasser.bypass()

    time.sleep(10)

    doc = etree.HTML(driver.html)

    total_page = int(doc.xpath('//a[@title="Last Page"]/@href')[0].split('=')[1])

    with ThreadPoolExecutor(1) as pool:
        for page in range(1, total_page + 1):
            pool.submit(_fetch, page, driver)

    logger.success('all done')
