from fastapi import FastAPI

from services.products_service import ProductsService

app = FastAPI(title="LeroyMerlin Categories API")

@app.get("/process_products")
def get_categories():
    service = ProductsService()
    results = service.process()  # returns the dict from your service
    return {"results": results}

#criar novo endpoitn aqui, com get, para testar saída ir no browser

#testar com curl localhost:8000
@app.get("/")
def teste():
    return {"status": "beleza"}

@app.get("/test-db")
def test_database_connection():
    """Endpoint para testar a conexão com o banco de dados."""
    try:
        with PostgresClient() as db:
            db.cur.execute("SELECT 1;") # Query simples para verificar a conexão
            db.cur.fetchone()
        return {"status": "success", "message": "Conexão com BD Jóia!"}
    except Exception as e:
        # Retorna um erro 500 se a conexão falhar
        raise HTTPException(status_code=500, detail=f"Erro na conexão com o banco de dados: {e}")

