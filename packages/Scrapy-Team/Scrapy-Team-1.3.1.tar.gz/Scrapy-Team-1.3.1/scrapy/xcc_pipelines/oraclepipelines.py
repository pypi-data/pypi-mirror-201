
"""
更新日期:2023/03/31
作者: D.Z.zhong
用途: oracle存储管道
运行环境：pip install oracledb==1.2.2 ; oracle库版本>11
item 对象须有属性 `database` `table`
eg.
class TestItem(scrapy.Item):
    database = "USER"
    table = "NUM_UPDATECSD"
    xxxxx = scrapy.Field()
"""
try:
    import oracledb
except:
    print("请尽快升级 scrapy-team >= 1.3.0 版本")
import os

from scrapy.utils.conf import get_config

import logging


class OraclePipeline:
    '''
    environment :python -m pip install oracledb==1.2.2 ; oracle version > 11
    item require some attributes : `database` `table`
    eg.
    class TestItem(scrapy.Item):
        database = "USER"
        table = "NUM_UPDATECSD"
        xxxxx = scrapy.Field()
    '''
    def __init__(self, host, user, password, port, service_name):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.service_name = service_name

    @classmethod
    def from_crawler(cls, crawler):
        # 判断运行环境<根据环境变量中是否配置IF_PROD=True,或 测试正式环境settings["IF_PROD"] = True>
        section_select ="oracle_cfg_prod" if os.environ.get('IF_PROD') == "True" or crawler.settings.get('IF_PROD')\
             == True or get_config().get("settings","IF_PROD",fallback="False")=="True" else "oracle_cfg_dev"
        # 取 scrapy.cfg 参与配置
        return cls(
            host=get_config().get(section=section_select,option="ORACLE_HOST",fallback='') or crawler.settings.get('ORACLE_HOST'),
            user=get_config().get(section=section_select,option='ORACLE_USER',fallback='') or crawler.settings.get('ORACLE_USER'),
            password=get_config().get(section=section_select,option='ORACLE_PASSWORD',fallback='') or crawler.settings.get('ORACLE_PASSWORD'),
            port=get_config().getint(section=section_select,option='ORACLE_PORT',fallback='') or crawler.settings.get('ORACLE_PORT'),
            service_name=get_config().getint(section=section_select,option='ORACLE_SERVICE',fallback='') or crawler.settings.get('ORACLE_SERVICE'),
        )

    def open_spider(self, spider):
        dsn = f'{self.user}/{self.password}@{self.host}:{self.port}/{self.service_name}'
        self.db = oracledb.connect(dsn)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join([":"+i for i in data.keys()])
        sql = 'INSERT INTO "% s"."% s" VALUES (% s)' % (item.database ,item.table, keys)
        try:
            self.cursor.execute(sql, list(data.values()))
            self.db.commit()
        except Exception as e:
            logging.warn(e)
        return item