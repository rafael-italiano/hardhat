from fastapi import FastAPI
import os
from clients.postgres_client import PostgresClient
app = FastAPI(title="LeroyMerlin Categories API")

@app.get("/")
def get_categories():
    dsn = os.getenv('DATABASE_URL', 'test')
    postgres = PostgresClient(dsn)
    return postgres.test()