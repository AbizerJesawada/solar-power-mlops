import pandas as pd
import yaml
import os

from src.logger import get_logger

logger = get_logger(__name__)

def load_params():
    with open("params.yaml") as f:
        return yaml.safe_load(f)

def ingest_data():
    params = load_params()

    logger.info("Loading generation data...")
    gen_df = pd.read_csv(params['data']['raw_generation'])

    logger.info("Loading weather data...")
    weather_df = pd.read_csv(params['data']['raw_weather'])

    logger.info("Generation Data Shape: %s", gen_df.shape)
    logger.info("Weather Data Shape: %s", weather_df.shape)
    
    return gen_df, weather_df

if __name__ == "__main__":
    gen_df, weather_df = ingest_data()
    logger.info("Data Ingestion Complete!")
