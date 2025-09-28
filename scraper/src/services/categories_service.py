from scrapy.crawler import CrawlerProcess

from services.base_service import BaseService
from spiders.categories_spider import LeroyMerlinCategoriesSpider

class LeroyMerlinCategoryService(BaseService):
    def __init__(self) -> None:
        self.results = []

    def _process_item(self, item) -> None:

        self.results.append(item)
        return None
    
    def process(self) -> list:

        process = CrawlerProcess()
        process.crawl(
            LeroyMerlinCategoriesSpider,
            item_callback=self._process_item
        )
        process.start()
        return self.results