import os
import sys
import time

from scrapy.crawler import CrawlerProcess
from multiprocessing import Process
from scrapy.utils.project import get_project_settings
from analyser_hj3415.db import mongo
from selenium.webdriver.remote.webdriver import WebDriver
import pandas as pd

from util_hj3415 import utils
from .nfs.spiders import common
from scrapy.selector import Selector
import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)


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


def _run_scrapy(spider: str, codes: list, mongo_addr: str):
    """
    scrapy 스파이더를 스크립트로 실행할 수 있는 함수
    :param spider:
    :param codes:
    :param mongo_addr:
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
    process.crawl(spider, code=codes, mongo_client=mongo_client)
    process.start()

    if mongo_client is not None:
        mongo_client.close()


def _mp_c10168(spider: str, codes: list, mongo_addr: str):
    """
    전체 코드를 코어수 대로 나눠서 멀티 프로세싱 시행
    reference from https://monkey3199.github.io/develop/python/2018/12/04/python-pararrel.html

    멀티프로세싱시 mongoclient를 만들어서 호출하는 방식은 에러가 발생하니 각 프로세스에서 개별적으로 생성해야한다.
    referred from https://blog.naver.com/PostView.nhn?blogId=stop2y&logNo=222211823932&categoryNo=136&parentCategoryNo=
    0&viewDate=&currentPage=1&postListTopCurrentPage=1&from=postView

    :param spider:
    :param codes:
    :param mongo_addr:
    :return:
    """

    if spider not in ('c101', 'c106', 'c108'):
        raise NameError
    print('*' * 25, f"Scrape multiprocess {spider.capitalize()}", '*' * 25)
    print(f'Total {len(codes)} items..')
    logger.info(codes)
    n, divided_list = utils.code_divider_by_cpu_core(codes)

    start_time = time.time()
    ths = []
    error = False
    for i in range(n):
        ths.append(Process(target=_run_scrapy, args=(spider, divided_list[i], mongo_addr)))
    for i in range(n):
        ths[i].start()
    for i in range(n):
        ths[i].join()
    print(f'Total spent time : {round(time.time() - start_time, 2)} sec.')


def _mp_c1034(page: str, codes: list, mongo_addr: str):
    """
    c103 6개, c104 8개 페이지수대로 멀티프로세싱 시행
    :param page:
    :param codes:
    :return:
    """
    if page == 'c103':
        spiders = ('c103_iy', 'c103_by', 'c103_cy', 'c103_iq', 'c103_bq', 'c103_cq')
    elif page == 'c104':
        spiders = ('c104_aq', 'c104_bq', 'c104_cq', 'c104_dq', 'c104_ay', 'c104_by', 'c104_cy', 'c104_dy')
    else:
        raise NameError
    title = spiders[0].split('_')[0]
    print('*' * 25, f"Scrape multiprocess {title}", '*' * 25)
    print(f'Total {len(codes)} items..')
    logger.info(codes)

    start_time = time.time()
    ths = []
    error = False
    for spider in spiders:
        ths.append(Process(target=_run_scrapy, args=(spider, codes, mongo_addr)))
    for i in range(len(ths)):
        ths[i].start()
    for i in range(len(ths)):
        ths[i].join()
    print(f'Total spent time : {round(time.time() - start_time, 2)} sec.')


@chcwd
def c101(codes: list, mongo_addr: str = ""):
    """
    c101을 외부에서 실행할 수 있는 함수
    :param codes: 종목코드 리스트
    :param mongo_addr: 몽고데이터베이스 URI - mongodb://...
    :return:
    """
    _mp_c10168('c101', codes=codes, mongo_addr=mongo_addr)


@chcwd
def c103(codes: list, mongo_addr: str = ""):
    """
    c103을 외부에서 실행할 수 있는 함수
    :param codes: 종목코드 리스트
    :param mongo_addr: 몽고데이터베이스 URI - mongodb://...
    :return:
    """
    test_driver = utils.get_driver()
    if test_driver is None:
        print("Fail to get chrome driver...Try again", file=sys.stderr)
    else:
        test_driver.close()
        _mp_c1034('c103', codes=codes, mongo_addr=mongo_addr)


@chcwd
def c104(codes: list, mongo_addr: str = ""):
    """
    c104을 외부에서 실행할 수 있는 함수
    :param codes: 종목코드 리스트
    :param mongo_addr: 몽고데이터베이스 URI - mongodb://...
    :return:
    """
    test_driver = utils.get_driver()
    if test_driver is None:
        print("Fail to get chrome driver...Try again", file=sys.stderr)
    else:
        test_driver.close()
        _mp_c1034('c104', codes=codes, mongo_addr=mongo_addr)


@chcwd
def c106(codes: list, mongo_addr: str = ""):
    """
    c106을 외부에서 실행할 수 있는 함수
    :param codes: 종목코드 리스트
    :param mongo_addr: 몽고데이터베이스 URI - mongodb://...
    :return:
    """
    test_driver = utils.get_driver()
    if test_driver is None:
        print("Fail to get chrome driver...Try again", file=sys.stderr)
    else:
        test_driver.close()
        _mp_c10168('c106', codes=codes, mongo_addr=mongo_addr)


"""
@chcwd
def c108(codes: list, mongo_addr: str = ""):
    _mp_c10168('c108', codes=codes, mongo_addr=mongo_addr)
"""

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

def scrape_c103_first_page(driver:WebDriver, code: str) -> pd.DataFrame:
    """
    코드에 해당하는 c103의 첫페이지인 포괄손익계산서y를 추출하여 df로 반환한다.
    해당 함수는 주로 코드의 내용이 바뀌었는지 확인하기 위해 사용한다.
    """
    if not utils.is_6digit(code):
        raise Exception(f"Invalid code format : {code}")

    url = f"https://navercomp.wisereport.co.kr/v2/company/c1030001.aspx?cmp_cd={code}"

    driver.implicitly_wait(5)
    driver.get(url)

    wait = WebDriverWait(driver, timeout=5)
    table_xpath = '//table[2]'
    wait.until(EC.visibility_of_element_located((By.XPATH, table_xpath)))

    html = Selector(text=driver.page_source)


    df = common.get_df_from_html(html, table_xpath, 1)
    return df
