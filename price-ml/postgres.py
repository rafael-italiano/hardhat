import psycopg
from psycopg.rows import dict_row

class PostgresClient(BaseClient):
    def __init__(self, dsn: str):

        self.dsn = dsn
        self.conn = psycopg.connect(self.dsn, row_factory=dict_row)

    def __enter__(self):
        self.conn = psycopg.connect(self.dsn, row_factory=dict_row)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

    def update_products(self, product_array):
        cur = self.conn.cursor()
        try:
            for p in product_array:
                cur.execute("""
                    INSERT INTO categories (name) 
                    VALUES (%s)
                    ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
                    RETURNING id;
                """, (p.category,))
                if row := cur.fetchone():
                    category_id = row["id"]

                cur.execute("""
                    INSERT INTO subcategories (name, category_id) 
                    VALUES (%s, %s)
                    ON CONFLICT (name, category_id) DO UPDATE SET name = EXCLUDED.name
                    RETURNING id;
                """, (p.subcategory, category_id))
                if row := cur.fetchone():
                    subcategory_id = row["id"]

                cur.execute("""
                    INSERT INTO brands (name) 
                    VALUES (%s)
                    ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
                    RETURNING id;
                """, (p.brand,))
                if row := cur.fetchone():
                    brand_id = row["id"]

                cur.execute("""
                    INSERT INTO products (
                        external_id, name, type, subcategory_id, brand_id, sellers, 
                        external_updated_at, url
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (external_id) DO UPDATE
                    SET name = EXCLUDED.name,
                        type = EXCLUDED.type,
                        subcategory_id = EXCLUDED.subcategory_id,
                        brand_id = EXCLUDED.brand_id,
                        sellers = EXCLUDED.sellers,
                        external_updated_at = EXCLUDED.external_updated_at,
                        url = EXCLUDED.url
                    RETURNING id;
                """, (
                    p.product_id, p.name, p.type, subcategory_id, brand_id,
                    p.sellers, p.updated_at, p.url
                ))
                if row := cur.fetchone():
                    product_db_id = row["id"]

                cur.execute("""
                    INSERT INTO prices (product_id, price)
                    VALUES (%s, %s);
                """, (product_db_id, p.price))

            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cur.close()