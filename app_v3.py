# -*- coding:utf-8 -*-

import requests
from loguru import logger
from lxml import etree
from tqdm import trange

from settings import *

logger.add(os.path.join(DUMP_DIR, 'tac_crawler_{time:YYYYMMDD}.log'), rotation="50 MB", retention="3 days",
           compression="gz", enqueue=True)


def _parse_rows(page_source):
    """
    直接用lxml解析表格，避免引入pandas。
    每行三列：TAC、Brand、Devices。Brand可能为空；Devices为<ul><li>列表，可能为空。
    返回 [(tac, brand, devices), ...]，devices多个型号以逗号连接。
    """
    page_doc = etree.HTML(page_source)
    rows = []
    for tr in page_doc.xpath('//table[contains(@class, "table")]/tbody/tr'):
        tds = tr.xpath('./td')
        if len(tds) < 3:
            continue

        # TAC 在第一列的<a>里
        tac = ''.join(tds[0].xpath('.//text()')).strip()
        # Brand 为第二列纯文本，空白项strip后为空字符串
        brand = ''.join(tds[1].xpath('.//text()')).strip()
        # Devices 为第三列<ul><li>列表，逐个取文本；空<ul>得到空列表
        devices = [t.strip() for t in tds[2].xpath('.//li//text()') if t.strip()]

        if not tac:
            continue

        rows.append((tac, brand, '  '.join(devices)))
    return rows


def _fetch(_page):
    retry = 0
    max_retry = 5
    while retry < max_retry:
        try:
            page_resp = requests.get(
                'http://192.168.185.83:4321/html?url=https://swappa.com/imei/tac?page={}'.format(_page))

            rows = _parse_rows(page_resp.text)

            if not rows:
                raise ValueError('page {} 未解析到任何数据，可能响应异常'.format(_page))

            with open(os.path.join(DUMP_DIR, 'tac_{ts}.text'.format(ts=TODAY)), mode='a', encoding='utf-8') as f:
                for tac, brand, devices in rows:
                    f.write('|'.join([tac, brand, devices]) + '\n')

            logger.success('page {} done', _page)
            retry = max_retry
        except Exception as e:
            logger.error(e)
            retry = retry + 1
            logger.error(f"第 {retry} 次失败，重试")
            for _ in trange(10 * retry):
                time.sleep(1)
        finally:
            pass


if __name__ == '__main__':

    resp = requests.get('http://192.168.185.83:4321/html?url=https://swappa.com/imei/tac')

    time.sleep(10)

    doc = etree.HTML(resp.text)

    total_page = int(doc.xpath('//a[@title="Last Page"]/@href')[0].split('=')[1])

    for page in range(1, total_page + 1):
        _fetch(page)
        time.sleep(10)

    logger.success('all done')
