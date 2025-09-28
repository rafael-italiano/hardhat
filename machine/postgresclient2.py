#cria e deleta tabelas, dados, etc, um para cada projeto esse doc
import psycopg2
import os
from psycopg2 import sql

os.getenv('DATABASE_URL', 'null')

class PostgresClient:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="postgres",
            user="postgres.leyzzpezasoqdkinogwk",
            password="Univesp@25",
            host="aws-1-sa-east-1.pooler.supabase.com",
            port=5432,
            sslmode='require'
        )
        self.cur = self.conn.cursor()

    def create_table(self, table_name, columns):
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({});").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(
                sql.SQL('{} {}').format(sql.Identifier(col), sql.SQL(dtype)) for col, dtype in columns.items()
            )
        )
        self.cur.execute(query)
        self.conn.commit()

    def drop_table(self, table_name):
        query = sql.SQL("DROP TABLE IF EXISTS {};").format(sql.Identifier(table_name))
        self.cur.execute(query)
        self.conn.commit()

    def insert_data(self, table_name, data):
        columns = data.keys()
        values = [data[col] for col in columns]
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({});").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(values))
        )
        self.cur.execute(query, values)
        self.conn.commit()

    def fetch_data(self, table_name):
        query = sql.SQL("SELECT * FROM {};").format(sql.Identifier(table_name))
        self.cur.execute(query)
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()
