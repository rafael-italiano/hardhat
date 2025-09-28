from clients.base_client import BaseAPI
from services.base_service import BaseService

class ProductsService(BaseService):

    def __init__(self, client:BaseAPI, category_service:BaseService):
        self.client = client
        self.category_service = category_service

    def process(self):

        categories_array = self.category_service.process()
        return categories_array