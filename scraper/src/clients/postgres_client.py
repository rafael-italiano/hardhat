import psycopg

from psycopg.rows import dict_row


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

    def insert(self, table: str, data: dict):
        """
        Insert a row into a table.
        :param table: Name of the table
        :param data: Dictionary of column -> value
        """
        if not self.conn:
            raise RuntimeError("Database connection is not established")

        columns = ", ".join(data.keys())
        placeholders = ", ".join([f"%({col})s" for col in data.keys()])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *;"

        with self.conn.cursor() as cur:
            cur.execute(query, data)
            self.conn.commit()
            return cur.fetchone()  # Return inserted row
        
    def test(self):
        query = "INSERT INTO test VALUES (34) RETURNING *;"

        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()
            return cur.fetchone()  # Return inserted row
        