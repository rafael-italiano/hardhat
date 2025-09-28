# Cliente para interagir com o banco de dados PostgreSQL.
import psycopg2
import os
from psycopg2 import sql

class PostgresClient:
    """
    Um cliente PostgreSQL que gerencia conexões e cursores
    usando gerenciadores de contexto para garantir o fechamento adequado dos recursos.
    As configurações de conexão são lidas a partir de variáveis de ambiente.
    """
    def __init__(self):
        # Carrega a string de conexão da variável de ambiente DATABASE_URL
        # ou usa valores padrão se não estiver definida.
        self.db_url = os.getenv('DATABASE_URL')
        if not self.db_url:
            # Fallback para variáveis individuais se DATABASE_URL não estiver definida
            self.db_url = (
                f"dbname={os.getenv('DB_NAME', 'postgres')} "
                f"user={os.getenv('DB_USER', 'postgres.leyzzpezasoqdkinogwk')} "
                f"password={os.getenv('DB_PASSWORD', 'Univesp@25')} "
                f"host={os.getenv('DB_HOST', 'aws-1-sa-east-1.pooler.supabase.com')} "
                f"port={os.getenv('DB_PORT', '5432')} "
                f"sslmode={os.getenv('DB_SSLMODE', 'require')}"
            )
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = psycopg2.connect(self.db_url)
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def commit(self):
        self.conn.commit()

    def create_table(self, table_name, columns):
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({});").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(
                sql.SQL('{} {}').format(sql.Identifier(col), sql.SQL(dtype)) for col, dtype in columns.items()
            )
        )
        self.cur.execute(query)

    def drop_table(self, table_name):
        query = sql.SQL("DROP TABLE IF EXISTS {};").format(sql.Identifier(table_name))
        self.cur.execute(query)

    def insert_data(self, table_name, data):
        columns = data.keys()
        values = [data[col] for col in columns]
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({});").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(values))
        )
        self.cur.execute(query, values)

    def fetch_data(self, table_name):
        query = sql.SQL("SELECT * FROM {};").format(sql.Identifier(table_name))
        self.cur.execute(query)
        return self.cur.fetchall()

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
