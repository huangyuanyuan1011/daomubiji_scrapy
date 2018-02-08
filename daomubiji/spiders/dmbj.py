# -*- coding: utf-8 -*-
import scrapy

from daomubiji.items import DaomubijiItem


class DmbjSpider(scrapy.Spider):
    name = 'dmbj'
    allowed_domains = ['www.daomubiji.com']
    start_urls = ['http://www.daomubiji.com/zang-hai-hua', 'http://www.daomubiji.com/sha-hai',
                  'http://www.daomubiji.com/dao-mu-bi-ji-2015', ]
    # start_urls = ['http://www.daomubiji.com/dao-mu-bi-ji-%d' % i for i in range(1, 9)]

    def parse(self, response):
        article_lists=response.xpath("//article[@class = 'excerpt excerpt-c3']")
        for article in article_lists:
            item = DaomubijiItem()
            chapter_name = article.xpath(".//a/text()").extract_first()
            chapter_urls = article.xpath(".//a/@href").extract_first()
            item['chapter_name'] =chapter_name
            item['chapter_urls'] = chapter_urls
            yield scrapy.Request(url=chapter_urls,meta={'item':item},callback=self.chapter_detail)

    def chapter_detail(self,response):
        item = response.meta['item']
        chapter_contents = response.xpath("//article[@class='article-content']//p/text()").extract()
        item['chapter_content'] = '\n'.join(chapter_contents)
        yield item



