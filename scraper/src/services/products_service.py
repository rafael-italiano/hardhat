from logging import getLogger

from clients.base_client import BaseAPI
from clients.base_client import BaseClient

from services.base_service import BaseService
from services.models import Product

logger = getLogger(__name__)

class ProductsService(BaseService):

    def __init__(self, client:BaseAPI, category_service:BaseService, database:BaseClient):
        self.client = client
        self.category_service = category_service
        self.database = database

    def process(self):

        categories = self.category_service.process()
        logger.info(f"Fetched {categories}")
        for category in categories:

            category_name = category['category']
            subcategory = category['subcategory']
            category_products=[]
            logger.info("Fetching new subcategory", extra=category)
            raw_products = self.client.get(category_name, subcategory)
            error_count = 0
            for product in raw_products:
                try:
                    product = Product(
                        name=product['name'],
                        type=product['attributes']['Produto'],
                        category=category_name,
                        subcategory=subcategory,
                        brand=product['attributes']['Marca'][0],
                        sellers=product['boitataFacets']['sellers'],
                        product_id=product['product_id'],
                        url=product['url'],
                        price=product['averagePromotionalPrice'],
                        updated_at=product['updatedAt'],
                    )
                except KeyError:
                    logger.error("Product insertion failed", extra={"record":product})
                    product = None
                    error_count += 1
                if product:
                    category_products.append(product)
            logger.info("Loading data into database", extra={"records": len(category_products)})
            if error_count:
                logger.warning(f"Failed to insert {error_count} records", extra= {'failed_inserts': error_count})
            self.database.update_products(category_products)
        return category_products