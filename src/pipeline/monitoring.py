import json
import os

import mlflow
import pandas as pd
import yaml

from src.logger import get_logger

logger = get_logger(__name__)


def load_params():
    with open("params.yaml") as f:
        return yaml.safe_load(f)


def calculate_feature_drift(reference_df, current_df, feature_columns, threshold_percent):
    drift_results = {}

    for feature in feature_columns:
        reference_mean = reference_df[feature].mean()
        current_mean = current_df[feature].mean()

        if reference_mean == 0:
            drift_percent = 0.0 if current_mean == 0 else 100.0
        else:
            drift_percent = abs((current_mean - reference_mean) / reference_mean) * 100

        drift_results[feature] = {
            "reference_mean": round(float(reference_mean), 4),
            "current_mean": round(float(current_mean), 4),
            "drift_percent": round(float(drift_percent), 4),
            "drift_detected": bool(drift_percent > threshold_percent),
        }

    return drift_results


def run_drift_monitoring():
    params = load_params()
    processed_path = params["data"]["processed"]
    feature_columns = params["model"]["features"]
    threshold_percent = params["monitoring"]["drift_threshold_percent"]
    report_path = params["output"]["drift_report_path"]

    logger.info("Running data drift monitoring...")
    df = pd.read_csv(processed_path)

    split_index = int(len(df) * 0.8)
    reference_df = df.iloc[:split_index]
    current_df = df.iloc[split_index:]

    drift_results = calculate_feature_drift(
        reference_df,
        current_df,
        feature_columns,
        threshold_percent,
    )

    drift_detected = any(
        result["drift_detected"] for result in drift_results.values()
    )

    report = {
        "threshold_percent": threshold_percent,
        "drift_detected": drift_detected,
        "features": drift_results,
    }

    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)

    mlflow.log_metric("drift_detected", int(drift_detected))
    mlflow.log_metric("drift_threshold_percent", threshold_percent)
    for feature, result in drift_results.items():
        mlflow.log_metric(f"drift_percent_{feature}", result["drift_percent"])
        mlflow.log_metric(
            f"drift_detected_{feature}",
            int(result["drift_detected"]),
        )
    mlflow.log_artifact(report_path, artifact_path="monitoring")

    logger.info("Drift detected: %s", drift_detected)
    logger.info("Drift report saved to %s", report_path)

    return report


if __name__ == "__main__":
    mlflow.set_experiment("solar-power-forecasting")
    with mlflow.start_run():
        run_drift_monitoring()
