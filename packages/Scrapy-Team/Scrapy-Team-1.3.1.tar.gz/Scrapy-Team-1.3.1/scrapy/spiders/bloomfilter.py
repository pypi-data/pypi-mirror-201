

from scrapy.xcc_pipelines.bloomfilter import BloomFilterPipeline
from scrapy_redis.spiders import RedisSpider

import scrapy


class BloomFilterSpider(scrapy.Spider):
    """
    BloomFilerSpider 基础功能同 Spider
    新增属性`bloomfilter`
    用法:

    检查字符串是否in集合
    self.bloomfilter.lookup(<somestr>) :: lookup(self, str_input:str) -> int(0,1)

    insert 集合
    self.bloomfilter.insert(<somestr>) :: insert(self, str_input:str) -> None
    
    throw to 集合 存在返回True 不存在insert并返回 False
    self.bloomfilter.throw(<somedict>) :: throw(self,item:dict) -> bool

    """
    @classmethod
    def from_crawler(self, crawler, *args, **kwargs):
        obj = super(BloomFilterSpider, self).from_crawler(crawler, *args, **kwargs)
        obj.init_bloomfilter(crawler)
        return obj


    def init_bloomfilter(self,crawler):
        self.bloomfilter = BloomFilterPipeline.from_crawler(crawler)

class BloomFilterRedisSpider(RedisSpider):
    """
    BloomFilerRedisSpider 基础功能同 RedisSpider
    新增属性`bloomfilter`
    用法:

    检查字符串是否in集合
    self.bloomfilter.lookup(<somestr>) :: lookup(self, str_input:str) -> int(0,1)

    insert 集合
    self.bloomfilter.insert(<somestr>) :: insert(self, str_input:str) -> None

    throw to 集合 存在返回True 不存在insert并返回 False
    self.bloomfilter.throw(<somedict>) :: throw(self,item:dict) -> bool

    """
    @classmethod
    def from_crawler(self, crawler, *args, **kwargs):
        obj = super(BloomFilterRedisSpider, self).from_crawler(crawler, *args, **kwargs)
        obj.init_bloomfilter(crawler)
        obj.setup_redis(crawler)
        return obj


    def init_bloomfilter(self,crawler):
        self.bloomfilter = BloomFilterPipeline.from_crawler(crawler)