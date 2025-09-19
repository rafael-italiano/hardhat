import scrapy
import json
from src.items import ConstructionMaterial

class MaterialsSpider(scrapy.Spider):
    name = 'materials'
    #start_urls = ['https://www.lowes.com/pl/building-supplies/4294934297?goToProdList=true']

    #Realizado com livros para teste. Testado e funcionando. Corrigir para Lowe's.

    start_urls = ['https://books.toscrape.com/'] 
    #custom_settings = {
        #'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
     #   'DOWNLOAD_DELAY': 2
    #}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_count = 0
        self.max_items = 20

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                },
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):
            #    products = response.css('div[data-testid="product-card"]')
      #  category = response.css('h1.styles__H1-sc-11vpuyu-0::text').get() or "Building Supplies"
      #  for idx, product in enumerate(products):
         #   if idx >= self.max_items:
         #       break
           # title = product.css('span.description-spn::text').get()
           # brand = product.css('span[data-testid="splp-prd-brd-nm"]::text').get()
          #  price = product.css('div[data-selector="splp-prd-act-$"]::text').get()
           # if not price:
            #    price = product.css('span.price-break').xpath('string(.)').get()
           # url = response.urljoin(product.css('a[data-testid="product-title"]::attr(href)').get())
           # sku = url.split('/')[-1]
            #yield ConstructionMaterial(
               # title=title,
               # brand=brand,
               # category=category,
               # url=url,
              #  sku=sku,
             #   price=price
            #)
        self.logger.info(f"Response status: {response.status}")
        self.logger.info(f"Response URL: {response.url}")
        
        if response.status == 200:
            self.logger.info(f"Page title: {response.css('title::text').get()}")
            books = response.css('article.product_pod')
            self.logger.info(f"Found {len(books)} books")
            
            category = "Books"
            
            for idx, book in enumerate(books):
                if idx >= self.max_items:
                    break
                    
                title = book.css('h3 a::attr(title)').get()
                if not title:
                    title = book.css('h3 a::text').get()
                    
                price = book.css('p.price_color::text').get()
                availability = book.css('p.instock.availability::text').getall()
                availability = ' '.join(availability).strip() if availability else "Available"
                
                url = response.urljoin(book.css('h3 a::attr(href)').get())
                sku = url.split('/')[-1] if url else str(idx)
                
                yield ConstructionMaterial(
                    title=title,
                    brand="Unknown",  # Livros não tem marca.
                    category=category,
                    url=url,
                    sku=sku,
                    price=price
                )
        else:
            self.logger.warning(f"Failed to access page: {response.status}")

    def parse_product(self, response):
        try:
            ld_json = response.xpath("//script[@type='application/ld+json']/text()").get()
            title = brand = category = price = None
            if ld_json:
                data = json.loads(ld_json)
                title = data.get("name")
                brand = data.get("brand", {}).get("name")
                category = data.get("category")
                if "offers" in data and isinstance(data["offers"], dict):
                    price = data["offers"].get("price")
            if not title:
                title = response.css('h1::text').get()
            if not brand:
                brand = response.css('span.brand::text').get()
            if not category:
                category = response.css('h1.styles__H1-sc-11vpuyu-0::text').get() or "Building Supplies"
            if not price:
                price = response.css('span[itemprop="price"]::text').get()

            sku = response.url.split('/')[-1]
            url = response.url

            yield ConstructionMaterial(
                title=title,
                brand=brand,
                category=category,
                url=url,
                sku=sku,
                price=price
            )
        except Exception as e:
            self.logger.warning(f"Erro ao processar produto em {response.url}: {e}")