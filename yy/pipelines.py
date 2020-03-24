# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook
import pymysql

class YyPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['省','市','区','名称','等级','性质','电话'])
    def process_item(self, item, spider):
        line = [item['province'],item['city'],item['region'],item['name'],item['level'],item['character'],item['contact']]
        self.ws.append(line)
        self.wb.save("yyInfo.xlsx")
        return item

class MysqlPipeline(object):
    """
    同步操作
    """
    def __init__(self):
        # 建立连接
        self.conn = pymysql.connect(host='192.168.123.100',port=32109,user='root',password='qzk7lWeyL4',db='spider',charset='utf8')
        # 创建游标
        self.cursor = self.conn.cursor()
 
    def process_item(self,item,spider):
        # sql语句
        insert_sql = """
        insert into yy(id,province,city,region,name,level,character,contact) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql,(item['province'],item['city'],item['region'],item['name'],item['level'],item['character'],item['contact']))
        # 提交，不进行提交无法保存到数据库
        self.conn.commit()
 
    def close_spider(self,spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()
