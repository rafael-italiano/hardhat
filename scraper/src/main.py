import atexit
import logging
import json
import os

from clients.leroy_merlin_client import LeroyMerlinClient
from clients.postgres_client import PostgresClient
from services.products_service import ProductsService
from services.categories_service import LeroyMerlinCategoryService

from clients.leroy_merlin_client_mock import LeroyMerlinClientMock
from services.categories_service_mock import LeroyMerlinCategoryServiceMock



logger = logging.getLogger("hardhat-scraper")
with open("logger/config.json") as f:
    config=json.load(f)
    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)


if __name__ == '__main__':

    dsn = os.getenv('DATABASE_URL')

    logger.info("Initializing services")
    postgres_client = PostgresClient(dsn)
    leroy_merlin_client = LeroyMerlinClientMock()
    category_service = LeroyMerlinCategoryServiceMock()
    service = ProductsService(
        client=leroy_merlin_client,
        category_service=category_service,
        database=postgres_client
    )
    service.process()