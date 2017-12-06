# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
import re
from taobaoSnack.items import taobaoSnackItem
from scrapy.selector import Selector
import urllib2
import string
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class TaobaoSpider(scrapy.Spider):
    name = "taobao"
    allowed_domanis = ["taobao.com"]
    start_urls = ['https://taobao.com/']

    # 获取商品页数url
    def parse(self,response):
        key = '小吃'
        for i in range(0, 3):
            url = 'https://s.taobao.com/search?q=' + str(key) + '&s=' + str(44*i)
            #print url
            yield Request(url=url,callback=self.page)
        pass

    # 解析每个商品的url
    def page(self,response):
        body = response.body.decode('utf-8','ignore')
        pattam_id = '"nid":"(.*?)"'
        pattam_shop= '"nick":"(.*?)"' 
        all_id = re.compile(pattam_id).findall(body)
        all_shop = re.compile(pattam_shop).findall(body)
        #print all_id
        for i in range(0,len(all_id)):
            this_id = all_id[i]
            shop = all_shop[i]
            url = 'https://item.taobao.com/item.htm?id=' + str(this_id)
            yield Request(url=url, callback=self.next,meta={'shop':shop})
            pass
        pass

    # 提取商品内容
    def next(self,response):
        #print response.url
        sel = Selector(response)
        url = response.url
        pattam_url = "http.*://(.*?).com"
        subdomain = re.compile(pattam_url).findall(url)
        #print subdomain
        item = taobaoSnackItem()
        # 提取商品名称
        if subdomain[0] != 'item.taobao':
            titles = sel.xpath("//div[@class='tb-detail-hd']/h1/text()").extract()
        else:
            titles = sel.xpath("//h3[@class='tb-main-title']/@data-title").extract()
        # 过滤\r\n\t字符
        titleall = []
        for title in titles:
            title = title.replace('\t','').replace('\r','').replace('\n','')
            titleall.append(title)
        #print titleall
        item['title'] = titleall
        # 提取店铺名称
        item['shop'] = response.meta['shop']
        # 提取商品链接
        item['link'] = response.url
        # 提取价格
        if subdomain[0] != 'item.taobao':
            pattam_price = '"defaultItemPrice":"(.*?)"'
            price = re.compile(pattam_price).findall(response.body.decode('utf-8','ignore'))
            #price = sel.xpath("//em[@class='tm-yen'/span[@class='tm-price'/text()").extract()
        else:
            price = sel.xpath("//em[@class='tb-rmb-num']/text()").extract()
        #print price
        item['price'] = price
        # 提取商品id
        if subdomain[0] != 'item.taobao':
            pattam_id = 'id=(.*?)&'
            this_id = re.compile(pattam_id).findall(url)[0]
        else:
            pattam_id = 'id=(.*?)$'
            this_id = re.compile(pattam_id).findall(url)[0]
        #print this_id
        # 提取评论数量
        comment_url = 'https://dsr-rate.tmall.com/list_dsr_info.htm?itemId='+ str(this_id)
        #print comment_url
        comment_data = urllib2.urlopen(comment_url).read().decode('utf-8','ignore')
        #print comment_data
        pattam_comment = '{.*?{.*?"rateTotal":(.*?)}}'
        comment = re.compile(pattam_comment).findall(comment_data)
        #print comment
        item['comment'] = comment
        yield item
    
