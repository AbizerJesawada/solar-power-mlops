import mlflow

from src.pipeline.data_ingestion import ingest_data
from src.pipeline.preprocessing import preprocess_data
from src.pipeline.train import train_model
from src.pipeline.evaluate import evaluate_model
from src.pipeline.monitoring import run_drift_monitoring

if __name__ == "__main__":
    print("Starting Solar Power MLOps Pipeline...")

    mlflow.set_experiment("solar-power-forecasting")

    with mlflow.start_run():
        # Step 1: Ingest
        gen_df, weather_df = ingest_data()

        # Step 2: Preprocess
        df = preprocess_data(gen_df, weather_df)

        # Step 3: Train
        model, X_test, y_test = train_model()

        # Step 4: Evaluate
        metrics = evaluate_model(model, X_test, y_test)

        # Step 5: Monitor
        drift_report = run_drift_monitoring()

    print("\nPipeline Complete!")
    print(f"Final Metrics: {metrics}")
    print(f"Drift Detected: {drift_report['drift_detected']}")
