# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
import re
from yy.items import YyItem

class Yyk99Spider(scrapy.Spider):
    name = 'yyk99'
    allowed_domains = ['yyk.99.com.cn']
    start_urls = ['https://yyk.99.com.cn/']
    domain = "https://yyk.99.com.cn"

    # 解析首页中省份页面
    def parse(self, response):
        res = Selector(response)
        regions = res.xpath("//div[@class='area-list']//a/@href").extract()
        for region in regions:
            yield scrapy.Request(url=str(self.domain+region),callback=self.parse2,dont_filter=True)
    # 解析省份页面中的医院地址
    def parse2(self,response):
        res = Selector(response)
        yys = res.xpath("//div[@class='g-warp']//a/@href").extract()
        urls = []
        for yy in yys:
            colection = []
            for item in self.get_province_url(yy,colection):
                urls.append(item)
        for item in urls:
            yield scrapy.Request(url=str(item),callback=self.parse3,dont_filter=True)
    # 解析医院详情页面的具体信息
    def parse3(self,response):
        res = Selector(response)
        item = YyItem()
        item['id']=str(response.request.url).split("/")[4]
        locations = res.xpath("//div[@class='crumb']//a/text()").extract()
        if len(locations)==4:
            item['province'] = locations[1]
            item['city'] = locations[2]
            item['region'] = locations[3]
        else:
            item['province'] = locations[1]
            item['city'] = locations[1]
            item['region'] = locations[2]
        item['name'] = res.xpath("//div[@class='wrap-mn']//h1/text()").extract_first()
        item['level'] = res.xpath("//span[@class='grade']/text()").extract_first()
        item['character'] = res.xpath("//div[@class='wrap-hd']//p[2]/text()").extract_first()[3:]
        #item['contact'] = res.xpath("/html[1]/body[1]/div[8]/div[1]/div[1]/dl[1]/dd[1]/p[3]/em[1]/text()").extract_first()
        #item['contact'] = res.css("div.wrapper:nth-child(10) div.wrap-hd div.wrap-mn dl.wrap-info:nth-child(4) dd:nth-child(2) p:nth-child(3) > em:nth-child(2)").extract()
        item['contact'] = res.xpath("//p[3]//em[1]/text()").extract_first()
        yield item
    # 剔除省份页面中非医院URL
    def get_province_url(self,content,colection):
        dit = re.compile("[0-9]")
        res = dit.search(content)
        if res:
            colection.append(str(self.domain+content))
        return colection
