CREATE DATABASE hardhat;
\c hardhat;

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT now() NOT NULL,
    updated_at TIMESTAMP DEFAULT now() NOT NULL
);

CREATE TABLE subcategories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category_id INT NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT now() NOT NULL,
    updated_at TIMESTAMP DEFAULT now() NOT NULL,
    UNIQUE (name, category_id)
);

CREATE TABLE brands (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT now() NOT NULL,
    updated_at TIMESTAMP DEFAULT now() NOT NULL
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    external_id BIGINT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    type TEXT,
    subcategory_id INT REFERENCES subcategories(id) ON DELETE SET NULL,
    brand_id INT REFERENCES brands(id) ON DELETE SET NULL,
    sellers TEXT[] NOT NULL, 
    external_updated_at TIMESTAMP NOT NULL,
    url TEXT,
    created_at TIMESTAMP DEFAULT now() NOT NULL,
    updated_at TIMESTAMP DEFAULT now() NOT NULL
);

CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    price NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT now() NOT NULL
);

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at_categories
BEFORE UPDATE ON categories
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER set_updated_at_subcategories
BEFORE UPDATE ON subcategories
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER set_updated_at_brands
BEFORE UPDATE ON brands
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER set_updated_at_products
BEFORE UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();
