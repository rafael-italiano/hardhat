import os
import sys
from dotenv import load_dotenv

# Para testar a conexão com o banco de dados, rodar o comando dentro do
# ambiente VENV: python database/test_db.py

# Adiciona o diretório raiz ao path e carrega o .env
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from postgresclient import PostgresClient

try:
    print("Tentando conectar ao banco de dados...")
    with PostgresClient() as db:
        db.cur.execute("SELECT 1;") # Query simples para testar a conexão
        result = db.cur.fetchone()
        if result and result[0] == 1:
            print("Conexão bem-sucedida!")
except Exception as e:
    print("Erro na conexão:", e)