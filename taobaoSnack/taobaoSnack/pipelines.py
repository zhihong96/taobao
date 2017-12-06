# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb.cursors
from twisted.enterprise import adbapi
from taobaoSnack import settings
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class TestContentPipline(object):
     def process_item(self, item, spider):
        title = item['title'][0]
        shop = item['shop']
        link = item['link']
        price = item['price'][0]
        comment = item['comment'][0]
        print "title:", title
        print "shop:", shop
        print "link:", link
        print "price:", price
        print "comment:",comment
        print "------------------------\n"
        return item

class TaobaoPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings["MYSQL_HOST"],
            port=settings["MYSQL_PORT"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWD"], 
            db=settings["MYSQL_DBNAME"],
            charset=settings["MYSQL_CHARSET"],
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert,item)
        query.addErrback(self._handle_error,item,spider)
        return item

    def _conditional_insert(self,tx,item):
        sql = "insert into snack(title,shop,link,price,comment) values(%s,%s,%s,%s,%s)"
        params = (item['title'][0],item['shop'],item['link'],
            item['price'][0],item['comment'][0])
        tx.execute(sql,params)

    def _handle_error(self,e,item,spider):
        print e
