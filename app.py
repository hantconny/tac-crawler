# -*- coding:utf-8 -*-
import time
from concurrent.futures import ThreadPoolExecutor
from io import StringIO

import cloudscraper
import pandas
from loguru import logger
from lxml import etree

from settings import *

logger.add(os.path.join(DUMP_DIR, 'tac_crawler_{time:YYYYMMDD}.log'), rotation="1 MB", retention="7 days",
           compression="gz", enqueue=True)


def _fetch(_page, _scraper):
    resp = _scraper.get('https://swappa.com/imei/tac?page={}'.format(_page))

    time.sleep(1)

    tables = pandas.read_html(StringIO(resp.text), converters={'TAC': str, 'Devices': str, 'Brand': str})

    with open(os.path.join(DUMP_DIR, 'tac_{ts}.text'.format(ts=TODAY)), mode='a', encoding='utf-8') as f:
        for table in tables:
            for line in zip(table['TAC'], table['Brand'], table['Devices']):
                tac, brand, devices = line
                # logger.debug(line)
                f.write('|'.join([tac, brand, devices]) + '\n')

    logger.success('page {} done', _page)


if __name__ == '__main__':

    scraper = cloudscraper.create_scraper()

    resp = scraper.get('https://swappa.com/imei/tac')

    doc = etree.HTML(resp.text)

    total_page = int(doc.xpath('//a[@title="Last Page"]/@href')[0].split('=')[1])

    with ThreadPoolExecutor(5) as pool:
        for page in range(1, total_page + 1):
            pool.submit(_fetch, page, scraper)

    logger.success('all done')
