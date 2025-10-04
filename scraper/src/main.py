import atexit
import logging
import json
import os

from clients.leroy_merlin_client import LeroyMerlinClient
from clients.postgres_client import PostgresClient
from services.products_service import ProductsService
from services.categories_service import LeroyMerlinCategoryService


logger = logging.getLogger("hardhat-scraper")
with open("logger/config.json") as f:
    config=json.load(f)
    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)

noisy_libs = ['httpcore.http11', 'httpcore.connection']
for lib in noisy_libs:
    logging.getLogger(lib).setLevel(logging.INFO)

logger.setLevel(logging.INFO)
if __name__ == '__main__':

    logger.setLevel(logging.INFO)
    dsn = os.getenv('DATABASE_URL')

    postgres_client = PostgresClient(dsn)
    leroy_merlin_client = LeroyMerlinClient()
    category_service = LeroyMerlinCategoryService()
    service = ProductsService(
        client=leroy_merlin_client,
        category_service=category_service,
        database=postgres_client
    )
    logger.info("Initiating product prices processing.")
    service.process()