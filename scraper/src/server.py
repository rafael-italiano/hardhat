from fastapi import FastAPI
import os
from clients.postgres_client import PostgresClient
from clients.leroy_merlin_client import LeroyMerlinClient
from clients.leroy_merlin_client_mock import LeroyMerlinClientMock
from services.products_service import ProductsService
from services.categories_service_mock import LeroyMerlinCategoryServiceMock
app = FastAPI(title="LeroyMerlin Categories API")


@app.get("/process")
def process_prices():
    dsn = os.getenv('DATABASE_URL', 'test')
    service = ProductsService(
        LeroyMerlinClientMock(),
        LeroyMerlinCategoryServiceMock(),
        PostgresClient(dsn=dsn)
    )
    service.process()