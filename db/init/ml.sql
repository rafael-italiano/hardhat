CREATE SCHEMA ml

CREATE TABLE ml.model (
    id SERIAL PRIMARY KEY,
    mse NUMERIC(12,2) NOT NULL,
    r2 NUMERIC(12,10) NOT NULL,
    created_at TIMESTAMP DEFAULT now() NOT NULL
);

CREATE TABLE ml.predicted_price (
    id SERIAL PRIMARY KEY,
    model_id INTEGER REFERENCES ml.model(id) ON DELETE SET NULL, 
    external_product_id NUMERIC(12,2) NOT NULL,
    prediction_date DATE NOT NULL,
    predicted_price NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT now() NOT NULL
);