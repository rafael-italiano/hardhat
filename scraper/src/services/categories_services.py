from scrapy.crawler import CrawlerProcess

from spiders.categories_spider import LeroyMerlinCategoriesSpider

class LeroyMerlinCategoryService:
    def __init__(self):
        self.results = []

    def process_item(self, item):
        """Armazena cada item coletado em memória"""
        self.results.append(item)

    def process(self):
        process = CrawlerProcess()

        # Passa a classe e injeta nosso callback de coleta de itens
        process.crawl(
            LeroyMerlinCategoriesSpider,
            item_callback=self.process_item  # passamos nosso método
        )
        process.start()  # bloqueia até o crawler terminar
        return self.results