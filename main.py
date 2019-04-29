import urllib

import scrapy
from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

import json

import settings as settings

nikeURL = 'https://www.nike.com.hk/man/new_release/list.htm?intpromo=PNTP'


class KithSpider(scrapy.Spider):
    name = 'kith'
    start_urls = [
        'https://kith.com/collections/mens-footwear',
    ]

    def parse(self, response):
        products = Selector(response).xpath('//*[@class="collection-product"]')
        for product in products:
            data = {}
            data['name'] = product.xpath('.//*[@class="product-card__title"]/text()').extract()[0]
            data['color'] = product.xpath('.//*[@class="product-card__color"]/text()').extract()[0]
            data['price'] = product.xpath('.//*[@class="product-card__price"]/text()').extract()[0].strip()
            data['img'] = product.xpath('//*[@class="ratio-box"]//img/@src').extract()[0]
            yield data


class NikehkSpider(scrapy.Spider):
    name = 'nikehk'
    start_urls = [nikeURL]

    def parse(self, response):
        products = Selector(response).xpath('//*[@class="style_liborder_new"]')

        for product in products:
            tempsku = product.xpath('.//*[@class="product_list_content"]/@code').extract()[0]
            form_data = {
                'skuCode': tempsku
            }
            yield scrapy.FormRequest('https://www.nike.com.hk/product/loadSameStyleData.json',
                                     callback=self.parse_url,
                                     method='POST', formdata=form_data,
                                     meta={'item': product})

    def parse_url(self, response):
        prevresponse = response.meta['item']
        jsonresponse = json.loads(response.body_as_unicode().replace("'", '"'))
        tempdata = jsonresponse['colors']

        for i in range(len(tempdata)):
            data = {}

            data['name'] = prevresponse.xpath('.//*[@class="up"]/text()').extract()[0]
            data['link'] = "https://www.nike.com.hk/" + \
                           prevresponse.xpath('.//*[@class="product_list_name"]/@href').extract()[0][1:]
            data['color'] = prevresponse.xpath('.//*[@class="new-sublist-all"]')
            data['price'] = prevresponse.xpath('.//*[@class="color666"]/text()').extract()[0].strip()
            data['img'] = "https://" + prevresponse.xpath('//*[@name="pdpAid"]//img/@lazy_src').extract()[0][2:]
            data['size'] = "N/A"
            data['skucode'] = jsonresponse['colors'][i]['code']
            yield data


if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    # process = CrawlerProcess({
    #     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    # })
    # process.crawl(KithSpider)
    process.crawl(NikehkSpider)
    process.start()  # the script will block here until the crawling is finished
