from fastapi import FastAPI

from services.products_service import ProductsService

app = FastAPI(title="LeroyMerlin Categories API")

@app.get("/process_products")
def get_categories():
    service = ProductsService()
    results = service.process()  # returns the dict from your service
    return {"results": results}