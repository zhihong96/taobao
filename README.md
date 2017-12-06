# 淘宝小吃数据抓取与分析

## 开发环境  
ubuntu 64位系统  
Python 2.7.12  
Scrapy 1.4.0  
MySQL-python 1.2.5

## 项目实现

    项目具体思路来源于： http://www.aobosir.com/blog/2016/12/26/python3-large-web-crawler-taobao-com-import-to-MySQL-database/
 
### 1. 创建项目  
scrapy startproject taobaoSnack
### 2. 构建Item  
`class taobaoSnackItem(scrapy.Item):  
    title = scrapy.Field() # 商品名称   
    shop = scrapy.Field() # 店铺名称   
    link = scrapy.Field() # 链接
    price = scrapy.Field() # 价格  
    comment = scrapy.Field() # 评论数量  
          
### 3. 分析网址结构


## 数据分析
