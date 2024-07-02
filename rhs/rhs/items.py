# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RhsItem(scrapy.Item):
    name = scrapy.Field()
    summary = scrapy.Field()
    ngcontent = scrapy.Field()
    size = scrapy.Field()
    growingConditions = scrapy.Field()
    colours = scrapy.Field()
    position = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

