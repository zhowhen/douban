# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class DoubanPipeline(object):
    def __init__(self, dbparams):
        # 连接数据库
        self.connect = pymysql.connect(
            host=dbparams['host'],
            port=dbparams['port'],
            db=dbparams['db'],
            user=dbparams['user'],
            passwd=dbparams['passwd'],
            charset=dbparams['charset'],
            use_unicode=dbparams['use_unicode']
        )
        # 通过cursor执行sql语句
        self.cursor = self.connect.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        # 读取settings里的配置，并创建实例
        dbparams = dict(
            host=crawler.settings.get('MYSQL_HOST'),
            db=crawler.settings.get('MYSQL_DBNAME'),
            user=crawler.settings.get('MYSQL_USER'),
            passwd=crawler.settings.get('MYSQL_PASSWD'),
            port=crawler.settings.get('MYSQL_POR'),
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            use_unicode=True,
        )
        return cls(dbparams)

    def process_item(self, item, spider):
        try:
            # 查重处理
            self.cursor.execute(
                """select * from douban where title = %s""",
                item['title'])
            # 是否有重复数据
            repetition = self.cursor.fetchone()
            # 重复
            if repetition:
                pass
            self.cursor.execute(
                    """INSERT INTO douban(title,bd,star,quote)
                    VALUES(%s,%s,%s,%s)""",
                    (item['title'],
                     item['bd'],
                     item['star'],
                     item['quote']
                    ))
            self.connect.commit()
        except Exception as e:
            print(e)
        return item

    def close_spider(self, spider):
        self.connect.close()