CREATE SCHEMA ml

CREATE TABLE ml.model (
    id SERIAL PRIMARY KEY,
    mse NUMERIC(12,2) NOT NULL,
    r2 NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT now() NOT NULL
);

CREATE TABLE ml.predict_prices (
    id SERIAL PRIMARY KEY,
    model_id INTEGER REFERENCES ml.model(id) ON DELETE SET NULL, 
    price_id NUMERIC(12,2) NOT NULL,
    date NUMERIC(12,2) NOT NULL,
    predicted_price TIMESTAMP DEFAULT now() NOT NULL
);