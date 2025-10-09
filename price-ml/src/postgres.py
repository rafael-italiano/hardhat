import psycopg_binary as psycopg
from psycopg_binary.rows import dict_row

class PostgresClient():
    def __init__(self, dsn: str):

        self.dsn = dsn
        self.conn = psycopg.connect(self.dsn, row_factory=dict_row)

    def __enter__(self):
        self.conn = psycopg.connect(self.dsn, row_factory=dict_row)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

    def get(self, query):
        
