import mlflow

from src.logger import get_logger
from src.pipeline.data_ingestion import ingest_data
from src.pipeline.preprocessing import preprocess_data
from src.pipeline.train import train_model
from src.pipeline.evaluate import evaluate_model
from src.pipeline.monitoring import run_drift_monitoring

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("Starting Solar Power MLOps Pipeline...")

    mlflow.set_experiment("solar-power-forecasting")

    with mlflow.start_run():
        mlflow.set_tags(
            {
                "project": "solar-power-mlops",
                "app_entrypoint": "app.py",
                "interface": "streamlit-dashboard",
                "deployment_target": "aws-ec2",
                "ci_pipeline": "github-actions",
            }
        )

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

    logger.info("Pipeline Complete!")
    logger.info("Final Metrics: %s", metrics)
    logger.info("Drift Detected: %s", drift_report["drift_detected"])
