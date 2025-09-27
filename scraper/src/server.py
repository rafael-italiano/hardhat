from fastapi import FastAPI
from services.categories_services import LeroyMerlinCategoryService

app = FastAPI(title="LeroyMerlin Categories API")

@app.get("/categories")
def get_categories():
    service = LeroyMerlinCategoryService()
    results = service.process()  # returns the dict from your service
    return {"categories": results}