import scrapy


class AmazonScrapyScrapperItem(scrapy.Item):
    detail = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    rating = scrapy.Field()
    type = scrapy.Field()
