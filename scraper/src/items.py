from scrapy import Field, Item

class ConstructionMaterial(Item):
    title = Field()
    brand = Field()
    category = Field()
    url = Field()
    sku = Field()
    price = Field()