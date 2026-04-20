import pandas as pd
import numpy as np
import pickle
import os
import yaml
import mlflow
import mlflow.sklearn
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split


def load_params():
    with open("params.yaml") as f:
        return yaml.safe_load(f)


def train_model():
    params = load_params()

    print("Loading processed data...")
    df = pd.read_csv(params['data']['processed'])

    feature_columns = params['model']['features']
    target_column = params['model']['target']

    X = df[feature_columns]
    y = df[target_column]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=params['model']['test_size'],
        random_state=params['model']['random_state']
    )
    
    print(f"Training samples: {X_train.shape[0]}")
    print(f"Testing samples: {X_test.shape[0]}")
    
    # MLflow tracking
    mlflow.set_experiment("solar-power-forecasting")
    
    with mlflow.start_run():
        print("Training XGBoost model...")
        model = XGBRegressor(
            n_estimators=params['model']['n_estimators'],
            max_depth=params['model']['max_depth'],
            learning_rate=params['model']['learning_rate']
        )
        model.fit(X_train, y_train)
        
        # Log parameters to MLflow
        mlflow.log_param("n_estimators", params['model']['n_estimators'])
        mlflow.log_param("max_depth", params['model']['max_depth'])
        mlflow.log_param("learning_rate", params['model']['learning_rate'])
        mlflow.log_param("test_size", params['model']['test_size'])
        mlflow.log_param("target", target_column)
        mlflow.log_param("features", ",".join(feature_columns))
        
        # Save model
        os.makedirs("models", exist_ok=True)
        with open(params['output']['model_path'], 'wb') as f:
            pickle.dump(model, f)
        
        mlflow.sklearn.log_model(
            sk_model=model,
            name="model",
            serialization_format=mlflow.sklearn.SERIALIZATION_FORMAT_SKOPS,
            skops_trusted_types=[
                "xgboost.core.Booster",
                "xgboost.sklearn.XGBRegressor",
            ],
        )
        print("Training Complete!")
    
    return model, X_test, y_test

if __name__ == "__main__":
    train_model()
