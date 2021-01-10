# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FiveOneJobItem(scrapy.Item):
    # define the fields for your item here like:

    job_name = scrapy.Field()     # 工作职位
    salary = scrapy.Field()       # 薪水
    city = scrapy.Field()         # 公司城市
    update_date = scrapy.Field()  # 更新时间
    company_type = scrapy.Field() # 公司类型
    work_year = scrapy.Field()    # 工作年限
    company_size = scrapy.Field() # 公司人数
    welfare = scrapy.Field()      # 福利
    degree = scrapy.Field()       # 学历
    recruit_num = scrapy.Field()  # 招聘人数