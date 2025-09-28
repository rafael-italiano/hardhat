import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os
import sys
from dotenv import load_dotenv

# Adiciona o diretório raiz do projeto ao path para encontrar o módulo `database`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Carrega as variáveis de ambiente do arquivo .env na raiz do projeto
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from database.postgresclient import PostgresClient

def fetch_data():
    """Busca os dados do banco de dados usando o PostgresClient."""
    with PostgresClient() as db:
        query = """
            SELECT pr.promotionalPrice, pr.originalPrice, pr.updatedAt, p.name, p.category_id
            FROM preco_vendedor pr
            JOIN produto p ON pr.product_id = p.product_id
        """
        # pd.read_sql pode usar a conexão diretamente
        df = pd.read_sql(query, db.conn)
        return df

def train_model(df):
    # Exemplo: prever preço promocional baseado no preço original e tempo
    df['updatedAt'] = pd.to_datetime(df['updatedAt']).astype(int) / 10**9
    X = df[['originalPrice', 'updatedAt']]
    y = df['promotionalPrice']
    model = LinearRegression()
    model.fit(X, y)
    joblib.dump(model, 'modelo_precos.pkl')

if __name__ == "__main__":
    df = fetch_data()
    train_model(df)