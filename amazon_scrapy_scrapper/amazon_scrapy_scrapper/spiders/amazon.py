import scrapy
from ..items import AmazonScrapyScrapperItem
import sys
from amazon_scrapy_scrapper.list import type_list

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.in']
    base_url = 'https://www.amazon.in'
    page_number = 2
    url_count = 1
    start_urls = [f'https://www.amazon.in/s?k={type_list[0]}&page=1']

    def get_data(response):
        
        detail = response.css('.a-size-medium.a-text-normal::text').extract()
        if len(detail) == 0:
            detail = response.css('.s-line-clamp-1 .a-color-base::text').extract()
        if len(detail) == 0:
            detail = response.css('.a-size-base-plus .a-color-base .a-text-normal::text').extract()

        price = response.css('.a-price-whole::text').extract()
        

        image = response.css('.s-image-fixed-height .s-image::attr(src)').extract()
        if len(image) == 0:
            image = response.css('.s-image::attr(src)').extract()

        ratings = response.css('.aok-align-bottom > .a-icon-alt::text').extract()
        
        rating_list = []
        for rating in ratings:
            splitted = rating.split(' ')
            rating_list.append(splitted[0])
        
        return [detail, price, image, rating_list]

    def parse(self, response):
        # brand = response.css('#brandsRefinements .s-navigation-item .a-color-base::text').extract()
        item = AmazonScrapyScrapperItem()
        data = AmazonSpider.get_data(response)
        item['detail'] = data[0] if data[0] else None
        item['price'] = data[1] if data[1] else None
        item['image'] = data[2] if data[2] else None
        item['rating'] = data[3] if data[3] else None
        item['type'] = type_list[AmazonSpider.url_count - 1]
        yield item

       
        if ((item['detail'] == None) and (item['price'] == None)):
            if (AmazonSpider.url_count == len(type_list)):
                sys.exit()
            
            AmazonSpider.page_number = 2
            type = type_list[AmazonSpider.url_count]
            AmazonSpider.url_count += 1
            yield scrapy.Request(f'https://www.amazon.in/s?k={type}&page=1', callback=self.parse)

        index = (response.url).index('&page')
        substr = response.url[:index]
        
        next_page = substr + '&page=' + str(AmazonSpider.page_number)
        
        AmazonSpider.page_number += 1
        yield response.follow(next_page, callback=self.parse)        
