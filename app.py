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
DRIFT_REPORT_PATH = Path("reports/drift_report.json")
DIAGRAMS_DIR = REPORTS_DIR / "report_assets"

PLOT_FILES = [
    ("Actual vs Predicted", "actual_vs_predicted.png"),
    ("Residual Distribution", "residual_distribution.png"),
    ("Residuals vs Predicted", "residuals_vs_predicted.png"),
    ("Evaluation Metrics", "evaluation_metrics.png"),
]

SUPPORTING_PLOTS = [
    ("Power Distribution", "ac_power_distribution.png"),
    ("Hourly Power Profile", "hourly_power.png"),
    ("Irradiation vs Power", "irradiation_vs_power.png"),
    ("Temperature vs Power", "temperature_vs_power.png"),
    ("Correlation Heatmap", "correlation_heatmap.png"),
]

DIAGRAM_FILES = [
    ("System Architecture", "system_architecture_diagram.png"),
    ("Pipeline Flow", "pipeline_flow_diagram.png"),
    ("Methodology", "methodology_diagram.png"),
]


def inject_styles():
    st.markdown(
        """
        <style>
        :root {
            --bg: #f4f1ea;
            --panel: rgba(255, 252, 247, 0.82);
            --panel-strong: #fffdf8;
            --stroke: rgba(59, 76, 64, 0.12);
            --text: #173126;
            --muted: #5f6f67;
            --accent: #1f7a4d;
            --accent-soft: #e6f3ea;
            --warm: #d29b49;
            --danger: #b35b41;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(210, 155, 73, 0.18), transparent 28%),
                radial-gradient(circle at top right, rgba(31, 122, 77, 0.14), transparent 30%),
                linear-gradient(180deg, #f8f4ed 0%, #f3efe7 48%, #eeeadf 100%);
            color: var(--text);
        }

        .block-container {
            padding-top: 1.4rem;
            padding-bottom: 2.5rem;
            max-width: 1250px;
        }

        div[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #183528 0%, #214634 100%);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        div[data-testid="stSidebar"] * {
            color: #f5f3ee !important;
        }

        .hero-shell {
            padding: 2rem 2.1rem;
            border: 1px solid var(--stroke);
            border-radius: 24px;
            background:
                linear-gradient(135deg, rgba(255, 255, 255, 0.93), rgba(246, 240, 230, 0.9)),
                linear-gradient(135deg, #ffffff, #f4efe4);
            box-shadow: 0 20px 40px rgba(38, 51, 43, 0.08);
            margin-bottom: 1.2rem;
        }

        .eyebrow {
            display: inline-block;
            padding: 0.35rem 0.7rem;
            border-radius: 999px;
            background: rgba(31, 122, 77, 0.1);
            color: var(--accent);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 0.8rem;
        }

        .hero-title {
            font-size: 2.55rem;
            line-height: 1.08;
            font-weight: 800;
            color: var(--text);
            margin: 0;
            max-width: 700px;
        }

        .hero-subtitle {
            margin-top: 0.9rem;
            max-width: 760px;
            color: var(--muted);
            font-size: 1.03rem;
            line-height: 1.65;
        }

        .hero-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.85rem;
            margin-top: 1.35rem;
        }

        .hero-stat, .glass-card, .status-card {
            background: var(--panel);
            backdrop-filter: blur(8px);
            border: 1px solid var(--stroke);
            border-radius: 20px;
            box-shadow: 0 12px 28px rgba(33, 47, 38, 0.06);
        }

        .hero-stat {
            padding: 1rem 1.1rem;
        }

        .hero-stat-label {
            font-size: 0.8rem;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.35rem;
        }

        .hero-stat-value {
            font-size: 1.35rem;
            font-weight: 800;
            color: var(--text);
        }

        .section-label {
            font-size: 0.8rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--accent);
            font-weight: 800;
            margin-top: 0.35rem;
            margin-bottom: 0.5rem;
        }

        .glass-card {
            padding: 1.15rem 1.2rem;
            margin-bottom: 1rem;
        }

        .glass-card h4, .status-title {
            margin: 0 0 0.35rem 0;
            color: var(--text);
        }

        .muted-copy {
            color: var(--muted);
            font-size: 0.95rem;
            line-height: 1.55;
        }

        .prediction-value {
            font-size: 2.25rem;
            font-weight: 900;
            color: var(--accent);
            margin: 0.15rem 0;
        }

        .status-card {
            padding: 1rem 1.1rem;
            min-height: 130px;
        }

        .status-value {
            font-size: 1.2rem;
            font-weight: 800;
            margin-top: 0.5rem;
            color: var(--text);
        }

        .status-ok {
            color: var(--accent);
        }

        .status-alert {
            color: var(--danger);
        }

        [data-testid="stMetric"] {
            background: var(--panel);
            border: 1px solid var(--stroke);
            border-radius: 18px;
            padding: 1rem;
            box-shadow: 0 10px 24px rgba(33, 47, 38, 0.05);
        }

        [data-testid="stMetricLabel"] {
            color: var(--muted);
        }

        [data-testid="stDataFrame"] {
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid var(--stroke);
            background: var(--panel-strong);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            margin-bottom: 0.65rem;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.5);
            border: 1px solid var(--stroke);
            padding: 0.4rem 0.95rem;
        }

        .stTabs [aria-selected="true"] {
            background: var(--accent-soft) !important;
            color: var(--accent) !important;
            border-color: rgba(31, 122, 77, 0.22) !important;
        }

        div[data-testid="stVerticalBlock"] div.stButton > button {
            background: linear-gradient(135deg, #1e6e47, #2f9158);
            color: white;
            border: none;
            border-radius: 999px;
            padding: 0.75rem 1.2rem;
            font-weight: 700;
            box-shadow: 0 14px 24px rgba(31, 122, 77, 0.22);
        }

        @media (max-width: 900px) {
            .hero-grid {
                grid-template-columns: 1fr;
            }
            .hero-title {
                font-size: 2rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


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


def load_drift_report():
    if not DRIFT_REPORT_PATH.exists():
        return None

    with DRIFT_REPORT_PATH.open() as drift_file:
        return json.load(drift_file)


def render_hero(metrics, target_column, feature_columns, drift_report):
    drift_detected = drift_report.get("drift_detected", False) if drift_report else False
    drift_label = "Stable data profile" if not drift_detected else "Drift requires review"
    r2_value = metrics.get("R2_Score", "NA") if metrics else "NA"

    st.markdown(
        f"""
        <section class="hero-shell">
            <div class="eyebrow">Solar Operations Intelligence</div>
            <h1 class="hero-title">Professional solar generation forecasting dashboard</h1>
            <p class="hero-subtitle">
                Estimate plant AC output from weather and time signals, review model quality,
                and inspect operational drift in a layout designed to feel closer to an energy
                control room than a demo notebook.
            </p>
            <div class="hero-grid">
                <div class="hero-stat">
                    <div class="hero-stat-label">Forecast Target</div>
                    <div class="hero-stat-value">{target_column}</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-label">Model Fit</div>
                    <div class="hero-stat-value">R² {r2_value}</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-label">Monitoring Status</div>
                    <div class="hero-stat-value">{drift_label}</div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("### Operations Panel")
        st.caption("Configure a forecast request and review deployment context.")
        st.markdown(f"**Target:** `{target_column}`")
        st.markdown(f"**Signals:** `{len(feature_columns)}` monitored inputs")
        st.markdown(f"**Model artifact:** `{MODEL_PATH}`")
        if metrics:
            st.markdown("**Current benchmark**")
            st.markdown(
                f"- RMSE: `{metrics.get('RMSE', 'NA')}`\n"
                f"- MAE: `{metrics.get('MAE', 'NA')}`\n"
                f"- R2: `{metrics.get('R2_Score', 'NA')}`"
            )
        if drift_report:
            status_text = "No significant drift detected" if not drift_detected else "Potential data drift detected"
            st.markdown("**Monitoring**")
            st.markdown(
                f"- Threshold: `{drift_report.get('threshold_percent', 'NA')}%`\n"
                f"- Status: `{status_text}`"
            )


def build_input_frame(feature_columns):
    st.markdown('<div class="section-label">Scenario Inputs</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="glass-card">
            <h4>Forecast scenario builder</h4>
            <div class="muted-copy">
                Enter operating conditions from the plant environment to estimate near-term
                AC power output. The controls are grouped to mirror weather and scheduling inputs.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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

    st.markdown('<div class="section-label">Model Quality</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("RMSE", metrics.get("RMSE", "NA"))
    col2.metric("MAE", metrics.get("MAE", "NA"))
    col3.metric("R2 Score", metrics.get("R2_Score", "NA"))


def show_evaluation_plots():
    st.markdown('<div class="section-label">Visual Validation</div>', unsafe_allow_html=True)

    for title, file_name in PLOT_FILES:
        image_path = REPORTS_DIR / file_name
        if image_path.exists():
            st.image(str(image_path), caption=title, width="stretch")
        else:
            st.warning(f"Missing plot: {file_name}. Run `python main.py` first.")


def show_supporting_plots():
    st.markdown('<div class="section-label">Operational Analytics</div>', unsafe_allow_html=True)
    plot_columns = st.columns(2)

    for index, (title, file_name) in enumerate(SUPPORTING_PLOTS):
        image_path = REPORTS_DIR / file_name
        with plot_columns[index % 2]:
            if image_path.exists():
                st.image(str(image_path), caption=title, width="stretch")
            else:
                st.warning(f"Missing plot: {file_name}.")


def show_drift_monitoring(drift_report):
    st.markdown('<div class="section-label">Monitoring</div>', unsafe_allow_html=True)

    if not drift_report:
        st.info("Drift report not available yet. Run `python main.py` to generate monitoring artifacts.")
        return

    threshold = drift_report.get("threshold_percent", "NA")
    drift_detected = drift_report.get("drift_detected", False)
    feature_rows = []
    for feature, details in drift_report.get("features", {}).items():
        feature_rows.append(
            {
                "Feature": feature,
                "Reference Mean": round(details.get("reference_mean", 0.0), 4),
                "Current Mean": round(details.get("current_mean", 0.0), 4),
                "Drift %": round(details.get("drift_percent", 0.0), 4),
                "Status": "Alert" if details.get("drift_detected") else "Stable",
            }
        )

    feature_df = pd.DataFrame(feature_rows).sort_values("Drift %", ascending=False)
    highest_drift = feature_df.iloc[0] if not feature_df.empty else None
    status_class = "status-alert" if drift_detected else "status-ok"
    status_text = "Data drift detected" if drift_detected else "Distribution stable"

    top_col1, top_col2, top_col3 = st.columns(3)
    with top_col1:
        st.markdown(
            f"""
            <div class="status-card">
                <div class="status-title">Monitoring status</div>
                <div class="muted-copy">Deployment health versus configured threshold.</div>
                <div class="status-value {status_class}">{status_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_col2:
        st.markdown(
            f"""
            <div class="status-card">
                <div class="status-title">Drift threshold</div>
                <div class="muted-copy">Configured tolerance before retraining review.</div>
                <div class="status-value">{threshold}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_col3:
        lead_feature = highest_drift["Feature"] if highest_drift is not None else "NA"
        lead_value = highest_drift["Drift %"] if highest_drift is not None else "NA"
        st.markdown(
            f"""
            <div class="status-card">
                <div class="status-title">Largest shift</div>
                <div class="muted-copy">Feature with the highest observed distribution change.</div>
                <div class="status-value">{lead_feature}: {lead_value}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.dataframe(feature_df, width="stretch", hide_index=True)


def show_system_diagrams():
    st.markdown('<div class="section-label">System View</div>', unsafe_allow_html=True)
    columns = st.columns(len(DIAGRAM_FILES))
    for column, (title, file_name) in zip(columns, DIAGRAM_FILES):
        image_path = DIAGRAMS_DIR / file_name
        with column:
            if image_path.exists():
                st.image(str(image_path), caption=title, width="stretch")
            else:
                st.warning(f"Missing diagram: {file_name}.")


def main():
    st.set_page_config(
        page_title="Solar Power Forecasting",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_styles()

    if not MODEL_PATH.exists():
        st.error("Model file not found. Run `python main.py` before starting the app.")
        st.stop()

    params = load_params()
    feature_columns = params["model"]["features"]
    target_column = params["model"]["target"]
    metrics = load_metrics()
    drift_report = load_drift_report()
    model = load_model()

    render_hero(metrics, target_column, feature_columns, drift_report)

    left_col, right_col = st.columns([1.05, 0.95], gap="large")

    with left_col:
        input_df = build_input_frame(feature_columns)
        st.markdown('<div class="section-label">Input Review</div>', unsafe_allow_html=True)
        st.dataframe(input_df, width="stretch", hide_index=True)

        predicted_value = None
        if st.button("Predict AC Power", type="primary", width="stretch"):
            predicted_value = float(model.predict(input_df)[0])
            st.session_state["predicted_value"] = predicted_value

        if "predicted_value" in st.session_state:
            predicted_value = st.session_state["predicted_value"]
            irradiation = float(input_df["IRRADIATION"].iloc[0])
            capacity_band = "Low generation regime"
            if predicted_value >= 200:
                capacity_band = "High generation regime"
            elif predicted_value >= 75:
                capacity_band = "Moderate generation regime"

            st.markdown(
                f"""
                <div class="glass-card">
                    <h4>Forecast result</h4>
                    <div class="muted-copy">Estimated plant AC output under the selected scenario.</div>
                    <div class="prediction-value">{predicted_value:.4f} kW</div>
                    <div class="muted-copy">
                        Operating interpretation: <strong>{capacity_band}</strong>.
                        Irradiation input is <strong>{irradiation:.4f}</strong>, which strongly influences output level.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with right_col:
        st.markdown(
            """
            <div class="section-label">Deployment Snapshot</div>
            <div class="glass-card">
                <h4>Inference environment</h4>
                <div class="muted-copy">
                    This app surfaces a production-style view of your trained solar power model,
                    combining forecasting, validation visuals, and monitoring artifacts in one place.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        show_metrics()
        show_drift_monitoring(drift_report)

    tabs = st.tabs(["Validation", "Analytics", "Architecture"])
    with tabs[0]:
        show_evaluation_plots()
    with tabs[1]:
        show_supporting_plots()
    with tabs[2]:
        show_system_diagrams()


if __name__ == "__main__":
    main()
