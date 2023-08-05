from itemadapter import ItemAdapter
from pprint import pprint
from analyser_hj3415.db import mongo

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)


class ValidationPipeline:
    def process_item(self, item, spider):
        print(f"\tIn the {self.__class__.__name__}...", end="")
        if spider.name == 'c101':
            print(f" Manual calculating EPS, BPS, PER, PBR")
            logger.debug('*** Start c101 pipeline ***')
            logger.debug(f"Raw data - EPS:{item['EPS']} BPS:{item['BPS']} PER:{item['PER']} PBR:{item['PBR']}")
            # eps, bps, per, pbr을 직접 계산해서 바꾸기 위해 c104 page를 찾는다.
            try:
                logger.debug('Try to get c104 page for calculate values..')
                c104q_data = mongo.C104(spider.mongo_client, item['코드'], 'c104q')
                d, eps = c104q_data.sum_recent_4q('EPS')  # 최근 4분기 eps값을 더한다.
                d, bps = c104q_data.latest_value('BPS')  # 마지막 분기 bps값을 찾는다.

                # per, pbr을 구하는 람다함수
                cal_ratio = (lambda eps_bps, pprice:
                             None if eps_bps is None or eps_bps == 0 else round(int(pprice) / int(eps_bps), 2))
                cal_per = cal_ratio(eps, item['주가'])
                cal_pbr = cal_ratio(bps, item['주가'])
                logger.debug(f"After calc data - EPS:{eps} BPS:{bps} PER:{cal_per} PBR:{cal_pbr}")
                logger.debug(f"*** End c101 calculation pipeline {item['코드']} ***")
            except:
                logger.warning("Error on calculating custom EPS, BPS, PER, PBR, maybe DB hasn't c104q collection.")
                logger.warning(
                    f"We will use default scraped values -  EPS:{item['EPS']} BPS:{item['BPS']} PER:{item['PER']} PBR:{item['PBR']}")
                return item
            item['EPS'], item['BPS'], item['PER'], item['PBR'] = eps, bps, cal_per, cal_pbr
        if 'c103' in spider.name:
            # pprint(item)
            print(" Nothing special for working")
        if 'c104' in spider.name:
            # pprint(item)
            print(" Nothing special for working")
        if spider.name == 'c106':
            # pprint(item)
            print(" Nothing special for working")
        return item


class MongoPipeline:
    def process_item(self, item, spider):
        print(f"\tIn the {self.__class__.__name__}...", end="")
        if spider.mongo_client is None:
            print(f"Skip for saving the data... code : {item['코드']} / spider : {spider.name}")
        else:
            print(f"Saving the {spider.name} to mongoDB...", end="")
            if spider.name == 'c101':
                page = spider.name
                print(f" code : {item['코드']} / page : {page}")
                mongo.C101(spider.mongo_client, item['코드']).save_dict(ItemAdapter(item).asdict())
            elif 'c103' in spider.name:
                page = ''.join(['c103', item['title']])
                print(f" code : {item['코드']} / page : {page}")
                logging.debug(item['df'].to_dict('records'))
                mongo.C103(spider.mongo_client, item['코드'], page).save_df(item['df'])
            elif 'c104' in spider.name:
                if item['title'].endswith('y'):
                    page = 'c104y'
                elif item['title'].endswith('q'):
                    page = 'c104q'
                else:
                    raise ValueError
                print(f" code : {item['코드']} / page : {page}({item['title']})")
                logging.debug(item['df'].to_dict('records'))
                mongo.C104(spider.mongo_client, item['코드'], page).save_df(item['df'])
            elif spider.name == 'c106':
                page = ''.join(['c106', item['title']])
                print(f" code : {item['코드']} / page : {page}")
                logging.debug(item['df'].to_dict('records'))
                if page == 'c106y':
                    mongo.C106(spider.mongo_client, item['코드'], 'c106y').save_df(item['df'])
                elif page == 'c106q':
                    mongo.C106(spider.mongo_client, item['코드'], 'c106q').save_df(item['df'])
                else:
                    raise
            """
            elif spider.name == 'c108':
                page = spider.name
                print(f" code : {item['코드']} / page : {page}")
                logging.debug(item['df'].to_dict('records'))
                r = mongo2.C108(self.client, item['코드']).save(item['df'])
            """
        return item
