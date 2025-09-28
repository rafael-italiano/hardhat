from scrapy import Field, Item


class LeroyMerlinCategory(Item):
    category = Field()
    subcategory = Field()
    url = Field()
