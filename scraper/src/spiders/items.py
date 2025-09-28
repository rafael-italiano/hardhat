# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class LeroyMerlinCategory(scrapy.Item):
    parent_category = scrapy.Field()
    subcategory_name = scrapy.Field()
    url = scrapy.Field()
