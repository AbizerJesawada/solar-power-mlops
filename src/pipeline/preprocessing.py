import pandas as pd
import os
import yaml

from src.logger import get_logger

logger = get_logger(__name__)

def load_params():
    with open("params.yaml") as f:
        return yaml.safe_load(f)

def preprocess_data(gen_df, weather_df):
    logger.info("Merging datasets...")
    gen_df['DATE_TIME'] = pd.to_datetime(gen_df['DATE_TIME'], dayfirst=True)
    weather_df['DATE_TIME'] = pd.to_datetime(weather_df['DATE_TIME'], dayfirst=False)
    
    df = pd.merge(gen_df, weather_df, on='DATE_TIME', how='inner')
    
    logger.info("Feature engineering...")
    df['HOUR'] = df['DATE_TIME'].dt.hour
    df['DAY'] = df['DATE_TIME'].dt.day
    df['MONTH'] = df['DATE_TIME'].dt.month
    
    # Drop unnecessary columns
    df.drop(columns=['DATE_TIME', 'PLANT_ID_x', 'PLANT_ID_y',
                     'SOURCE_KEY_x', 'SOURCE_KEY_y'],
            inplace=True, errors='ignore')
    
    # Drop nulls
    df.dropna(inplace=True)
    
    logger.info("Processed Data Shape: %s", df.shape)
    
    # Save processed data
    params = load_params()
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(params['data']['processed'], index=False)
    logger.info("Preprocessing Complete!")
    
    return df

if __name__ == "__main__":
    from data_ingestion import ingest_data
    gen_df, weather_df = ingest_data()
    df = preprocess_data(gen_df, weather_df)
    logger.info("Processed data preview:\n%s", df.head())
