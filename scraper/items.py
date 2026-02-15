import scrapy

class ScraperItem(scrapy.Item):
    source = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
    pivot_score = scrapy.Field()
