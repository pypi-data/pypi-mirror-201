import unittest
from src.scraper2_hj3415.krx import krx
from analyser_hj3415.db import mongo
from src.scraper2_hj3415.miscrapy import run as mirun


class MiscrapyTests(unittest.TestCase):
    def setUp(self):
        self.mongo_addr = "mongodb://192.168.0.173:27017"
        # self.mongo_addr = ""

    def test_one_spider(self):
        # spiders = ('aud', 'chf', 'gbond3y', 'gold', 'kosdaq', 'kospi', 'silver', 'sp500', 'usdidx', 'usdkrw', 'wti',)
        mirun._mi_test_one('chf', self.mongo_addr)

    def test_mi_all(self):
        mirun.mi_all()
        mirun.mi_all(self.mongo_addr)

    def test_avg_per(self):
        print(mirun.avg_per(mongo.connect_mongo(self.mongo_addr)))

    def test_yield_gap(self):
        avg_per = mirun.avg_per(mongo.connect_mongo(self.mongo_addr))
        print(mirun.yield_gap(mongo.connect_mongo(self.mongo_addr), avg_per))

    def test_mi_history(self):
        mirun.mi_history(1, self.mongo_addr)
