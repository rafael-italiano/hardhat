from clients.base_client import BaseAPI
from services.base_service import BaseService
from services.models import Product

class ProductsService(BaseService):

    def __init__(self, client:BaseAPI, category_service:BaseService):
        self.client = client
        self.category_service = category_service

    def process(self):

        categories = self.category_service.process()

        for category in categories:

            category_name = category['category']
            subcategory = category['subcategory']
            raw_products = self.client.get(category_name,subcategory)
            category_products = [
                Product(
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
                ) for product in raw_products
            ]
            break #insert into DB. Log.
        return category_products