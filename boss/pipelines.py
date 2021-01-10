# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BossPipeline(object):
    def process_item(self, item, spider):
        return item


import pymysql


# pipeline连接mysql数据库
class MysqlPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='123456', db='boss', charset='utf8')

        self.cursor = self.conn.cursor()
        print("successfull connected !!!")

    def process_item(self, item, spider):
        insert_sql = """
        insert into 51table(job_name,salary,city,update_date,company_type,work_year,company_size,welfare,degree,recruit_num) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        values = (
            item["job_name"], item['salary'], item['city'], item['update_date'], item['company_type'],
            item['work_year'],item['company_size'],
            item['welfare'], item["degree"], item["recruit_num"])
        self.cursor.execute(insert_sql, values)
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
