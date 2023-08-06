from analyser_hj3415.db import mongo

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

# 한개의 스파이더에서 연속 3일분량의 데이터가 전달된다.


class ValidationPipeline:
    def process_item(self, item, spider):
        print(" Nothing special for working")
        return item


class MongoPipeline:
    # 몽고 데이터 베이스에 저장하는 파이프라인
    def process_item(self, item, spider):
        """
        아이템 구조
            title = scrapy.Field()
            date = scrapy.Field()
            value = scrapy.Field()
        """
        print(f"\tIn the {self.__class__.__name__}...", end="")
        if spider.mongo_client is None:
            print(f"Skip for saving the data... date : {item['date']} / title : {item['title']} / value : {item['value']}")
        else:
            print(f"Saving the {spider.name} to mongoDB...date : {item['date']} / title : {item['title']} / value : {item['value']}")
            mongo.MI(spider.mongo_client, item['title']).save_dict({"date": item['date'], "value": item['value']})
        return item
