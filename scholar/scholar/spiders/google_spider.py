# -*- coding: utf-8 -*-
import scrapy
import scholar.items as items
from scrapy.http import Request


class GoogleSpiderSpider(scrapy.Spider):
    name = 'google_spider'
    allowed_domains = ['scholar.google.com.sg']

    def __init__(self,category=None, *args, **kwargs):
        super(GoogleSpiderSpider, self).__init__(*args, **kwargs)
        self.origin_urls = ['http://scholar.google.com.sg']
        self.start_urls = ['%s' % category]
        self.essay_list = []
        # ...

    def parse(self, response):
        essay_list = []
        html = response.xpath("/html/body")
        #tagget = html.xpath(".//div[@class='gs_r']/h3[@class='gs_rt']/a")
        #next_url = tagget[0].attrib["href"]
        #yield Request(self.origin_urls[0] + next_url, callback=self.parse_page)
        person_essay = html.xpath(".//tr[@class='gsc_a_tr']/td[@class='gsc_a_t']/a")
        for essay in person_essay:
            essay_list.append(essay.xpath('string()').extract()[0])
        self.essay_list = essay_list
        return self.essay_list

    # def parse_page(self, response):
    #     html = response.xpath("/html/body")
    #     person_list = html.xpath(".//h3[@class='gsc_oai_name']/a")
    #     for person in person_list:
    #         person_href = person.attrib["href"]
    #         request = yield Request(self.origin_urls[0] + person_href + "cstart=0&pagesize=10000", callback=self.parse_person)
    #     return request

    # def parse_person(self, response):
    #     essay_list = []
    #     item = items.ScholarItem()
    #     html = response.xpath("/html/body")
    #     person_essay = html.xpath(".//tr[@class='gsc_a_tr']/td[@class='gsc_a_t']/a")
    #     for essay in person_essay:
    #         essay_list.append(essay.xpath('string()').extract()[0])
    #     item['essay_list'] = self.essay_list + essay_list
    #     item['number'] = len(self.essay_list + essay_list)
    #     self.essay_list += essay_list
    #     return item