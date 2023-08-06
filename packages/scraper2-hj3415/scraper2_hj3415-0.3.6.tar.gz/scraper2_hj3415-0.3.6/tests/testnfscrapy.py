import unittest

from util_hj3415 import utils

from src.scraper2_hj3415.krx import krx
from src.scraper2_hj3415.nfscrapy import run as nfsrun


class NfscrapyTests(unittest.TestCase):
    def setUp(self):
        self.code_one = "005930"
        #self.code_one = ""
        self.mongo_addr = "mongodb://192.168.0.173:27017"
        #self.mongo_addr = ""
        self.rnd_code_list = krx.pick_rnd_x_code(2)

    def test_c101(self):
        if self.code_one:
            print(self.code_one)
            nfsrun.c101([self.code_one,])
        else:
            print(self.rnd_code_list)
            nfsrun.c101(self.rnd_code_list)
        if self.mongo_addr:
            nfsrun.c101(self.rnd_code_list, self.mongo_addr)

    def test_c103(self):
        if self.code_one:
            print(self.code_one)
            nfsrun.c103([self.code_one,])
        else:
            print(self.rnd_code_list)
            nfsrun.c103(self.rnd_code_list)
        if self.mongo_addr:
            nfsrun.c103(self.rnd_code_list, self.mongo_addr)
            
    def test_c104(self):
        if self.code_one:
            print(self.code_one)
            nfsrun.c104([self.code_one,])
        else:
            print(self.rnd_code_list)
            nfsrun.c104(self.rnd_code_list)
        if self.mongo_addr:
            nfsrun.c104(self.rnd_code_list, self.mongo_addr)

    def test_c106(self):
        if self.code_one:
            print(self.code_one)
            nfsrun.c106([self.code_one,])
        else:
            print(self.rnd_code_list)
            nfsrun.c106(self.rnd_code_list)
        if self.mongo_addr:
            nfsrun.c106(self.rnd_code_list, self.mongo_addr)

    def test_c10346_making_error(self):
        # 올바른 종목이 아닌경우
        err_code = '000000'
        nfsrun.c106([err_code, ])
        nfsrun.c103([err_code, ])
        nfsrun.c104([err_code, ])

    def test_scrape_c103_first_page(self):
        driver = utils.get_driver()
        print(nfsrun.scrape_c103_first_page(driver, '005930'))
