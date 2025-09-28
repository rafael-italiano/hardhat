import scrapy
from .items import LeroyMerlinCategory

class LeroyMerlinCategoriesSpider(scrapy.Spider):
    name = "leroy_categories"
    allowed_domains = ["leroymerlin.com.br"]
    start_urls = ["https://www.leroymerlin.com.br/materiais-de-construcao"]
    def __init__(self, item_callback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_callback = item_callback


    def parse(self, response):
        
        categories = response.css("div.flex.touch-pan-y a")
        for cat in categories:
            name = cat.css("p::text").get()
            if url := cat.attrib.get("href"):
                yield response.follow(
                    url,
                    callback=self.parse_subcategories,
                    meta={"category_name": name.strip() if name else None},
                )

    def parse_subcategories(self, response):
        parent_category = response.meta["category_name"]

        subcategories = response.css("a.flex.w-32.shrink-0.flex-col")

        for sub in subcategories:
            name = sub.css("p::text").get()
            url = sub.attrib.get("href")
            item = LeroyMerlinCategory(
                parent_category=parent_category,
                subcategory_name=name.strip() if name else None,
                url= response.urljoin(url) if url else None,
            )
            if self.item_callback:
                self.item_callback(item)  # envia para o serviço
            yield item