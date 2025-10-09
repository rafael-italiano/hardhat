import atexit
import os
import logging
import logging.config
import json

import pandas as pd
import psycopg
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sqlalchemy import create_engine, Engine

# Set up logging
logger = logging.getLogger("ml")
with open("logger/config.json") as f:
    config=json.load(f)
    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)

# Set up constants
DATABASE_URL = os.getenv('DATABASE_URL')
with open('training.sql', 'r') as f:
    SQL_QUERY = "".join(f.readlines())

def train_model(df):

    df['price_date'] = pd.to_datetime(df['price_date'])
    df['external_id'] = df['external_id'].astype('int64')
    df['subcategory_id'] = df['subcategory_id'].astype('int64')

    min_date = df['price_date'].min()
    df['days_since_start'] = (df['price_date'] - min_date).dt.days
    df = df.drop(columns=['price_date'])

    categorical_cols = ['external_id', 'subcategory_id']

    for col in categorical_cols:
        df[col] = df[col].astype(str)

    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    y = df['daily_average_price']
    X = df.drop(columns=['daily_average_price']) 

    X_train, X_test, y_train, y_test = train_test_split(
        X, 
        y, 
        test_size=0.2, 
        random_state=42
    )
    model = LinearRegression()
    logger.info("Initiating model training")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Mean Squared Error (MSE): {mse:,.4f}")
    print(f"R-squared (R2) Score: {r2:.4f}")
    coefficients = pd.Series(model.coef_, index=X.columns).sort_values(ascending=False)
    print(coefficients.head(10))
    return {
        'mse': mse,
        'r2': r2,
        'model': model
    }

if __name__ == '__main__':

    # Extract data
    engine:Engine = create_engine(DATABASE_URL)
    try:
        with engine.connect() as conn:
            df = pd.read_sql(SQL_QUERY, conn)
    except Exception as e:
        logger.error(f"Error executing query or loading data: {e}")
    
    trained_model = train_model(df)
