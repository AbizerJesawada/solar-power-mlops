import json
import pickle
from pathlib import Path

import pandas as pd
import streamlit as st
import yaml


MODEL_PATH = Path("models/model.pkl")
METRICS_PATH = Path("reports/metrics.json")
REPORTS_DIR = Path("reports")
PARAMS_PATH = Path("params.yaml")

PLOT_FILES = [
    ("Actual vs Predicted", "actual_vs_predicted.png"),
    ("Residual Distribution", "residual_distribution.png"),
    ("Residuals vs Predicted", "residuals_vs_predicted.png"),
    ("Evaluation Metrics", "evaluation_metrics.png"),
]


@st.cache_data
def load_params():
    with PARAMS_PATH.open() as params_file:
        return yaml.safe_load(params_file)


@st.cache_resource
def load_model():
    with MODEL_PATH.open("rb") as model_file:
        return pickle.load(model_file)


def load_metrics():
    if not METRICS_PATH.exists():
        return None

    with METRICS_PATH.open() as metrics_file:
        return json.load(metrics_file)


def build_input_frame(feature_columns):
    st.subheader("Prediction Inputs")

    col1, col2 = st.columns(2)

    with col1:
        ambient_temp = st.number_input(
            "Ambient Temperature", value=25.18, format="%.2f"
        )
        module_temp = st.number_input(
            "Module Temperature", value=22.85, format="%.2f"
        )
        irradiation = st.number_input(
            "Irradiation", min_value=0.0, value=0.0, format="%.4f"
        )

    with col2:
        hour = st.number_input("Hour", min_value=0, max_value=23, value=0)
        day = st.number_input("Day", min_value=1, max_value=31, value=15)
        month = st.number_input("Month", min_value=1, max_value=12, value=5)

    values = {
        "AMBIENT_TEMPERATURE": ambient_temp,
        "MODULE_TEMPERATURE": module_temp,
        "IRRADIATION": irradiation,
        "HOUR": hour,
        "DAY": day,
        "MONTH": month,
    }

    return pd.DataFrame([values], columns=feature_columns)


def show_metrics():
    metrics = load_metrics()
    if not metrics:
        st.info("Run `python main.py` first to generate evaluation metrics.")
        return

    st.subheader("Model Evaluation")
    col1, col2, col3 = st.columns(3)
    col1.metric("RMSE", metrics.get("RMSE", "NA"))
    col2.metric("MAE", metrics.get("MAE", "NA"))
    col3.metric("R2 Score", metrics.get("R2_Score", "NA"))


def show_evaluation_plots():
    st.subheader("Evaluation Visualizations")

    for title, file_name in PLOT_FILES:
        image_path = REPORTS_DIR / file_name
        if image_path.exists():
            st.image(str(image_path), caption=title, use_container_width=True)
        else:
            st.warning(f"Missing plot: {file_name}. Run `python main.py` first.")


def main():
    st.set_page_config(
        page_title="Solar Power Forecasting",
        layout="wide",
    )

    st.title("Solar Power Generation Forecasting")
    st.caption("End-to-end MLOps demo with DVC, MLflow, XGBoost, and Streamlit")

    if not MODEL_PATH.exists():
        st.error("Model file not found. Run `python main.py` before starting the app.")
        st.stop()

    params = load_params()
    feature_columns = params["model"]["features"]
    target_column = params["model"]["target"]

    st.write(f"Forecast target: `{target_column}`")

    model = load_model()
    input_df = build_input_frame(feature_columns)

    st.subheader("Input Preview")
    st.dataframe(input_df, use_container_width=True)

    if st.button("Predict AC Power", type="primary"):
        prediction = model.predict(input_df)[0]
        st.success(f"Predicted AC Power: {float(prediction):.4f} kW")

    show_metrics()
    show_evaluation_plots()


if __name__ == "__main__":
    main()
