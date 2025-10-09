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
from sqlalchemy import create_engine, Engine, text

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

def extract_data(engine: Engine) -> pd.DataFrame:

    try:
        with engine.connect() as conn:
            return pd.read_sql(SQL_QUERY, conn)
    except Exception as e:
        logger.error(f"Error executing query or loading data: {e}")

def train_model(df):
    """
    Prepares data, trains the Linear Regression model, calculates R2 and MSE, 
    and returns the results in a dictionary.
    """
    
    df_train = df.copy() 
    
    df_train['price_date'] = pd.to_datetime(df_train['price_date'])
    min_date = df_train['price_date'].min()
    df_train['days_since_start'] = (df_train['price_date'] - min_date).dt.days
    df_train = df_train.drop(columns=['price_date'])

    categorical_cols = ['external_id', 'subcategory_id']
    for col in categorical_cols:
        df_train[col] = df_train[col].astype(str)

    df_train = pd.get_dummies(df_train, columns=categorical_cols, drop_first=True)

    y = df_train['daily_average_price']
    X = df_train.drop(columns=['daily_average_price'])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    return {
        'model': model,
        'feature_columns': X.columns.tolist(),
        'mse': mse,
        'r2': r2
    }

def predict_next_day(df, model, feature_columns):
    """
    Creates the input data for the next day, generates predictions, 
    and returns a DataFrame of the results.
    """
    
    df['price_date'] = pd.to_datetime(df['price_date'])
    df['external_id'] = df['external_id'].astype(str)
    df['subcategory_id'] = df['subcategory_id'].astype(str)

    latest_date = df['price_date'].max()
    prediction_date = latest_date + pd.Timedelta(days=1)
    
    min_date = df['price_date'].min()
    prediction_days_since_start = (prediction_date - min_date).days

    last_day_data = df[df['price_date'] == latest_date].copy()
    
    last_prices = last_day_data[['external_id', 'daily_average_price']].set_index('external_id')
    
    X_predict_base = pd.DataFrame(last_prices.index)
    
    X_predict_base = X_predict_base.merge(last_prices, on='external_id')
    X_predict_base = X_predict_base.rename(columns={'daily_average_price': 'previous_day_average_price'})
    
    X_predict_base = X_predict_base.merge(
        last_day_data[['external_id', 'subcategory_id']].drop_duplicates(), 
        on='external_id', 
        how='left'
    )
    
    X_predict = pd.get_dummies(X_predict_base, columns=['external_id', 'subcategory_id'], drop_first=True)
    
    X_predict['days_since_start'] = prediction_days_since_start
    
    X_predict_aligned = pd.DataFrame(0, index=X_predict.index, columns=feature_columns)
    
    for col in X_predict.columns:
        if col in X_predict_aligned.columns:
            X_predict_aligned[col] = X_predict[col]

    next_day_predictions = model.predict(X_predict_aligned)

    results_df = X_predict_base[['external_id', 'previous_day_average_price']].copy()
    results_df['prediction_date'] = prediction_date
    results_df['predicted_daily_average_price'] = next_day_predictions
    
    return results_df[['prediction_date', 'external_id', 'predicted_daily_average_price']]

def store_model_statistics(engine: Engine, metrics: dict[str]) -> None:

    r2_score = metrics['r2']
    mse_value = metrics['mse']

    # SQL INSERT statement using parameter binding
    sql_insert = text("""
        INSERT INTO ml.model (r2, mse)
        VALUES (:r2_score, :mse_value)
        RETURNING id;
    """)

    try:
        with engine.connect() as connection:
            result = connection.execute(
                sql_insert, 
                {"r2_score": r2_score, "mse_value": mse_value}
            )
            # Commit the transaction to save the data
            connection.commit() 
            
            # Get the ID of the newly inserted row
            new_id = result.scalar_one()
            
            print(f"✅ Successfully stored model statistics (ID: {new_id}) in ml.models.")
            return new_id
            
    except Exception as e:
        print(f"❌ Error storing statistics in database: {e}")
        return None

def store_predictions(
    predictions_df: pd.DataFrame, 
    model_db_id: int, 
    engine: Engine
) -> None:
    """
    Stores the predicted prices from the DataFrame into the ml.predicted_price table.

    Args:
        predictions_df: DataFrame containing 'external_id', 'prediction_date', and 'predicted_daily_average_price'.
        model_db_id: The ID of the model from the ml.models table.
        engine: The SQLAlchemy engine connected to PostgreSQL.
    """
    
    df_insert = predictions_df.copy()
    
    df_insert = df_insert.rename(columns={
        'external_id': 'external_product_id',
        'predicted_daily_average_price': 'predicted_price'
    })
    
    df_insert['external_product_id'] = df_insert['external_product_id'].astype(float)
    df_insert['predicted_price'] = df_insert['predicted_price'].round(2)
    df_insert['prediction_date'] = pd.to_datetime(df_insert['prediction_date']).dt.date

    # Add the foreign key model_id
    df_insert['model_id'] = model_db_id
    
    # Select only the columns needed, in the correct order (optional but good practice)
    columns_to_insert = [
        'model_id', 
        'external_product_id', 
        'prediction_date', 
        'predicted_price'
    ]
    df_insert = df_insert[columns_to_insert]
    
    logger.info(f"Attempting to insert {len(df_insert)} predictions...")
    
    try:
        with engine.connect() as connection:
            df_insert.to_sql(
                'predicted_price', 
                con=connection, 
                schema='ml',
                if_exists='append',  # Add new rows
                index=False          # Don't write the DataFrame index
            )
            
        logger.info(f"✅ Successfully stored {len(df_insert)} predictions for model ID {model_db_id}.")
        
    except Exception as e:
        logger.error(f"❌ Error storing predictions in database: {e}")
    return

def main() -> None:

    engine:Engine = create_engine(DATABASE_URL)
    df = extract_data(engine)
    if df.empty:
        logger.error("Failed to extract data.")
        return
    
    logger.info("Training model...")
    training_results = train_model(df)
    logger.info(f"Model trained successfully. R2: {training_results['r2']}, MSE: {training_results['mse']}")

    predictions_df = predict_next_day(df, training_results['model'], training_results['feature_columns'])
    logger.info("Prices predicted successfully.")
    if predictions_df.empty:
        return
    model_id = store_model_statistics(engine, training_results)
    if not model_id:
        return
    store_predictions(predictions_df, model_id, engine)
    logger.info("Finished predictions.")
    
if __name__ == '__main__':
    main()