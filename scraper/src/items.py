# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item

class RefrigeratorItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Refrigerator(Item):
  title = Field()
  brand = Field()
  category = Field()
  url = Field()
  sku = Field()