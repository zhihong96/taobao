淘宝小吃数据抓取与分析
====
开发环境
--------
    ubuntu 64位系统
    Python 2.7.12
    Scrapy 1.4.0
    MySQL-python 1.2.5

项目实现
---------
    项目具体思路来源于： http://www.aobosir.com/blog/2016/12/26/python3-large-web-crawler-taobao-com-import-to-MySQL-database/
 
    1. 创建项目
     scrapy startproject taobaoSnack
    2. 构建Item
    class taobaoSnackItem(scrapy.Item):
        title = scrapy.Field()  # 商品名称
        shop = scrapy.Field()   # 店面名称
        link = scrapy.Field()   # 链接
        price = scrapy.Field()  # 价格
        comment = scrapy.Field() # 评论数量

    3. 分析网址结构
      当我们点击页面进行浏览时，我们发现不同的页面的网址有规律，并且下面是我们找到的规律：
      红色部分是一模一样的。
      删除红色部分，将剩下的组成网址，一样可以正常的浏览原网页。
      q= 后面是“小吃”的编码形式。
      s= 后面的数值等于 44*(当前页面-1)


数据分析
-----------
