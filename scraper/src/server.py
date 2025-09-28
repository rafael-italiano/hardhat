from fastapi import FastAPI

from clients.leroy_merlin_client import LeroyMerlinClient
from services.categories_service import LeroyMerlinCategoryService
from services.categories_service_mock import LeroyMerlinCategoryServiceMock
from services.products_service import ProductsService
from services.products_service_mock import ProductsServiceMock

app = FastAPI(title="LeroyMerlin Categories API")

@app.get("/")
def get_categories():
    service = ProductsServiceMock()
    return service.process()