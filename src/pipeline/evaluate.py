import numpy as np
import json
import os
import yaml
import mlflow
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from src.logger import get_logger

logger = get_logger(__name__)

def load_params():
    with open("params.yaml") as f:
        return yaml.safe_load(f)

def create_evaluation_visualizations(y_test, y_pred, metrics, reports_dir="reports"):
    os.makedirs(reports_dir, exist_ok=True)

    residuals = y_test - y_pred

    # Plot 1: Actual vs Predicted AC Power
    plt.figure(figsize=(8, 8))
    sns.scatterplot(x=y_test, y=y_pred, alpha=0.3, color="teal", edgecolor=None)
    min_value = min(y_test.min(), y_pred.min())
    max_value = max(y_test.max(), y_pred.max())
    plt.plot([min_value, max_value], [min_value, max_value], color="red", linewidth=2)
    plt.title("Actual vs Predicted AC Power")
    plt.xlabel("Actual AC Power (kW)")
    plt.ylabel("Predicted AC Power (kW)")
    plt.tight_layout()
    actual_vs_predicted_path = os.path.join(reports_dir, "actual_vs_predicted.png")
    plt.savefig(actual_vs_predicted_path)
    plt.close()
    logger.info("Evaluation plot saved: actual_vs_predicted.png")

    # Plot 2: Residual Distribution
    plt.figure(figsize=(10, 5))
    sns.histplot(residuals, bins=50, kde=True, color="slateblue")
    plt.axvline(0, color="red", linestyle="--", linewidth=2)
    plt.title("Residual Distribution")
    plt.xlabel("Residual Error")
    plt.ylabel("Frequency")
    plt.tight_layout()
    residual_distribution_path = os.path.join(reports_dir, "residual_distribution.png")
    plt.savefig(residual_distribution_path)
    plt.close()
    logger.info("Evaluation plot saved: residual_distribution.png")

    # Plot 3: Residuals vs Predicted AC Power
    plt.figure(figsize=(10, 5))
    sns.scatterplot(x=y_pred, y=residuals, alpha=0.3, color="darkorange", edgecolor=None)
    plt.axhline(0, color="red", linestyle="--", linewidth=2)
    plt.title("Residuals vs Predicted AC Power")
    plt.xlabel("Predicted AC Power (kW)")
    plt.ylabel("Residual Error")
    plt.tight_layout()
    residuals_vs_predicted_path = os.path.join(reports_dir, "residuals_vs_predicted.png")
    plt.savefig(residuals_vs_predicted_path)
    plt.close()
    logger.info("Evaluation plot saved: residuals_vs_predicted.png")

    # Plot 4: Evaluation Metrics
    plt.figure(figsize=(8, 5))
    metric_names = list(metrics.keys())
    metric_values = list(metrics.values())
    sns.barplot(x=metric_names, y=metric_values, color="steelblue")
    plt.title("Evaluation Metrics")
    plt.xlabel("Metric")
    plt.ylabel("Value")
    plt.tight_layout()
    metrics_path = os.path.join(reports_dir, "evaluation_metrics.png")
    plt.savefig(metrics_path)
    plt.close()
    logger.info("Evaluation plot saved: evaluation_metrics.png")

    return [
        actual_vs_predicted_path,
        residual_distribution_path,
        residuals_vs_predicted_path,
        metrics_path,
    ]

def evaluate_model(model, X_test, y_test):
    params = load_params()
    
    logger.info("Evaluating model...")
    y_pred = model.predict(X_test)
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    metrics = {
        "RMSE": float(round(rmse, 4)),
        "MAE": float(round(mae, 4)),
        "R2_Score": float(round(r2, 4))
    }
    
    logger.info("RMSE: %.4f", rmse)
    logger.info("MAE: %.4f", mae)
    logger.info("R2 Score: %.4f", r2)

    reports_dir = os.path.dirname(params['output']['reports_path']) or "."
    plot_paths = create_evaluation_visualizations(y_test, y_pred, metrics, reports_dir)

    # Log to MLflow
    mlflow.log_metric("RMSE", rmse)
    mlflow.log_metric("MAE", mae)
    mlflow.log_metric("R2_Score", r2)
    for plot_path in plot_paths:
        mlflow.log_artifact(plot_path, artifact_path="evaluation_plots")
    
    # Save metrics to JSON
    os.makedirs("reports", exist_ok=True)
    with open(params['output']['reports_path'], 'w') as f:
        json.dump(metrics, f, indent=4)
    
    logger.info("Evaluation Complete!")
    return metrics

if __name__ == "__main__":
    from train import train_model
    mlflow.set_experiment("solar-power-forecasting")
    with mlflow.start_run():
        model, X_test, y_test = train_model()
        evaluate_model(model, X_test, y_test)
