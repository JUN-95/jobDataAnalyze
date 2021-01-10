import json

import scrapy
from boss.items import FiveOneJobItem
import re
from lxml import etree


class FileOneJobSpider(scrapy.Spider):
    name = 'boss'
    allowed_domains = ['51job.com']
    start_urls = [
        'https://search.51job.com/list/030200,000000,0000,00,9,99,java,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=']
    total_page = 0
    curr_page = 1
    join_url = 'https://search.51job.com/list/030200,000000,0000,00,9,99,java,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='

    def parse(self, response):
        item = FiveOneJobItem()
        selection = etree.HTML(response.text)
        row_dict = selection.xpath("//script[@type='text/javascript']/text()")[0].split(" = ")[1]
        # print(row_dict)
        format_dict = json.loads(row_dict)
        print(format_dict)
        for dic in format_dict["engine_search_result"]:
            item["job_name"] = dic["job_name"]
            item["salary"] = dic["providesalary_text"]
            if dic["workarea_text"] != "":
                item["city"] = dic["workarea_text"]
            item["update_date"] = dic["updatedate"]
            if dic["companytype_text"] != "":
                item["company_type"] = dic["companytype_text"]
            if dic["companysize_text"] != "":
                item["company_size"] = dic["companysize_text"]
            if dic["jobwelf"] != "":
                item["welfare"] = dic["jobwelf"]
            list_info = dic["attribute_text"]
            print("list_info=========>"+str(list_info))
            try:
                if len(list_info) == 4:
                    item["work_year"] = list_info[1]
                    item["degree"] = list_info[2]
                    item["recruit_num"] = list_info[3]
                if len(list_info) == 3:
                    item["degree"] = list_info[1]
                    item["recruit_num"] = list_info[2]
            except RuntimeError:
                print("*******************" + str(list_info))
            yield item
        self.total_page = format_dict["total_page"]
        if self.curr_page < int(self.total_page):
            self.curr_page += 1
            self.join_url = 'https://search.51job.com/list/030200,000000,0000,00,9,99,java,2,' + \
                            str(self.curr_page) + \
                            '.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
        yield scrapy.Request(url=self.join_url, callback=self.parse)


