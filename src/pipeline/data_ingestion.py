import pandas as pd
import yaml
import os

def load_params():
    with open("params.yaml") as f:
        return yaml.safe_load(f)

def ingest_data():
    params = load_params()
    
    print("Loading generation data...")
    gen_df = pd.read_csv(params['data']['raw_generation'])
    
    print("Loading weather data...")
    weather_df = pd.read_csv(params['data']['raw_weather'])
    
    print(f"Generation Data Shape: {gen_df.shape}")
    print(f"Weather Data Shape: {weather_df.shape}")
    
    return gen_df, weather_df

if __name__ == "__main__":
    gen_df, weather_df = ingest_data()
    print("Data Ingestion Complete!")