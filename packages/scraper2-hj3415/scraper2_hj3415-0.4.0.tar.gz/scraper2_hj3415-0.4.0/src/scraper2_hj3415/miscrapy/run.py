import os
import sys
import time
import math
import datetime

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process

from analyser_hj3415.db import mongo
from analyser_hj3415 import eval
from util_hj3415 import utils

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)


def chcwd(func):
    """
    scrapy는 항상 프로젝트 내부에서 실행해야 하기 때문에 일시적으로 현재 실행 경로를 변경해주는 목적의 데코레이션 함수
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        before_cwd = os.getcwd()
        logger.info(f'current path : {before_cwd}')
        after_cwd = os.path.dirname(os.path.realpath(__file__))
        logger.info(f'change path to {after_cwd}')
        os.chdir(after_cwd)
        func(*args, **kwargs)
        logger.info(f'restore path to {before_cwd}')
        os.chdir(before_cwd)

    return wrapper


spider_list = ('aud', 'chf', 'gbond3y', 'gold', 'kosdaq', 'kospi', 'silver', 'sp500', 'usdidx', 'usdkrw', 'wti',)


def _run_scrapy(spider: str, mongo_addr: str):
    if mongo_addr == "":
        mongo_client = None
    else:
        try:
            mongo_client = mongo.connect_mongo(mongo_addr)
        except mongo.UnableConnectServerException:
            conn_str = f"Unable to connect to the server.(MY IP : {utils.get_ip_addr()})"
            print(f"{conn_str} Server Addr : {mongo_addr}", file=sys.stderr)
            return

    # reference from https://docs.scrapy.org/en/latest/topics/practices.html(코드로 스파이더 실행하기)
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider, mongo_client=mongo_client)
    process.start()

    if mongo_client is not None:
        mongo_client.close()


@chcwd
def _mi_test_one(spider: str, mongo_addr: str = ""):
    """
    각 mi 항목을 테스트해 보기 위한 테스트함수
    :param spider:
    :param mongo_addr:
    :return:
    """
    _run_scrapy(spider=spider, mongo_addr=mongo_addr)


@chcwd
def mi_all(mongo_addr: str = ""):
    """
    모든 mi 항목을 스크랩하는 함수
    :param mongo_addr:
    :return:
    """

    print('*' * 25, f"Scrape multiprocess mi", '*' * 25)
    logger.info(spider_list)

    start_time = time.time()
    ths = []
    error = False
    for spider in spider_list:
        ths.append(Process(target=_run_scrapy, args=(spider, mongo_addr)))
    for i in range(len(ths)):
        ths[i].start()
    for i in range(len(ths)):
        ths[i].join()
        if ths[i].exitcode != 0:
            error = True

    if mongo_addr == "":
        print('*' * 25, f"Skip for calculating the avgper and yieldgap", '*' * 25)
        return
    else:
        try:
            mongo_client = mongo.connect_mongo(mongo_addr)
        except mongo.UnableConnectServerException:
            conn_str = f"Unable to connect to the server.(MY IP : {utils.get_ip_addr()})"
            print(f"{conn_str} Server Addr : {mongo_addr}", file=sys.stderr)
            return

    # calc 모듈을 이용해서 avg_per 과 yield_gap 을 계산하여 저장한다.
    print('*' * 25, f"Calculate and save avgper and yieldgap", '*' * 25)

    mi_db = mongo.MI(mongo_client, 'avgper')

    today_str = datetime.datetime.today().strftime('%Y.%m.%d')

    # avg_per 계산 및 저장
    avgper = avg_per(mongo_client)
    avgper_dict = {'date': today_str, 'value': avgper}
    logger.info(avgper_dict)
    mi_db.save_dict(mi_dict=avgper_dict)
    print(f'\tSave to mongo... date : {today_str} / title : avgper / value : {avgper}')

    # yield_gap 계산 및 저장
    yieldgap = yield_gap(mongo_client, avgper)
    yieldgap_dict = {'date': today_str, 'value': yieldgap}
    logger.info(yieldgap_dict)
    mi_db.index = 'yieldgap'
    mi_db.save_dict(mi_dict=yieldgap_dict)
    print(f'\tSave to mongo... date : {today_str} / title : yieldgap / value : {yieldgap}')

    print(f'Total spent time : {round(time.time() - start_time, 2)} sec')
    print('done.')
    return error


@chcwd
def mi_history(year: int, mongo_addr: str = ""):
    """
    과거의 mi 항목들을 수집하기 위한 함수
    :param mongo_addr:
    :param year: 원하는 년수(1년전까지 자료를 원하면 1)
    :return:
    """
    if mongo_addr == "":
        mongo_client = None
    else:
        try:
            mongo_client = mongo.connect_mongo(mongo_addr)
        except mongo.UnableConnectServerException:
            conn_str = f"Unable to connect to the server.(MY IP : {utils.get_ip_addr()})"
            print(f"{conn_str} Server Addr : {mongo_addr}", file=sys.stderr)
            return

    process = CrawlerProcess(get_project_settings())
    process.crawl('mihistory', mongo_client, year=year)
    process.start()


"""
avgper 과 yieldgap 계산
"""


def avg_per(client) -> float:
    # 가중조화평균으로 평균 per 산출 mi db에 저장
    per_r_cap_all = []
    cap_all = []
    eval_list = eval.make_today_eval_df(client).to_dict('records')
    for data in eval_list:
        # eval data: {'code': '111870', '종목명': 'KH 일렉트론', '주가': 1070, 'PER': -2.28, 'PBR': 0.96,
        # '시가총액': 103300000000, 'RED': -11055.0, '주주수익률': -7.13, '이익지표': -0.30426, 'ROIC': -40.31,
        # 'ROE': 0.0, 'PFCF': -7.7, 'PCR': nan}
        logger.debug(f'eval data: {data}')
        if math.isnan(data['PER']) or data['PER'] == 0:
            continue
        if math.isnan(data['시가총액']):
            continue
        cap_all.append(data['시가총액'])
        per_r_cap_all.append((1 / data['PER']) * data['시가총액'])
    logger.debug(f'Count cap_all :{len(cap_all)}')
    logger.debug(f'Count per_r_cap_all : {len(per_r_cap_all)}')
    try:
        return round(sum(cap_all) / sum(per_r_cap_all), 2)
    except ZeroDivisionError:
        return float('nan')


def yield_gap(client, avgper: float) -> float:
    # 장고에서 사용할 yield gap, mi db에 저장
    logger.info(f"avg_per : {avgper}")
    mi_db = mongo.MI(client, index='gbond3y')
    date, gbond3y = mi_db.get_recent()
    logger.info(f"gbond3y : {date} / {gbond3y}")
    if math.isnan(avgper) or avgper == 0:
        return float('nan')
    else:
        yield_share = (1 / avgper) * 100
        yieldgap = round(yield_share - utils.to_float(gbond3y), 2)
        logger.debug(f"Date - {date}, gbond3y - {gbond3y}, yield_gap - {yieldgap}")
        return yieldgap
