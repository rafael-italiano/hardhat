import scrapy


class LeroyCategoriesSpider(scrapy.Spider):
    name = "leroy_categories"
    allowed_domains = ["leroymerlin.com.br"]
    start_urls = ["https://www.leroymerlin.com.br/"]

    def parse(self, response):
        # Seleciona todos os links dentro do carrossel de categorias
        categories = response.css(
            "div.flex.touch-pan-y a"
        )

        for cat in categories:
            yield {
                "name": cat.css("p::text").get().strip(),
                "url": response.urljoin(cat.attrib.get("href")),
                "image": cat.css("img::attr(src)").get()
            }
