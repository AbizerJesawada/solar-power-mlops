from __future__ import annotations

import json
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"
OUTPUT = REPORTS_DIR / "Solar_Power_MLOps_Project_Report.docx"
ASSETS_DIR = REPORTS_DIR / "report_assets"

REPO_URL = "https://github.com/AbizerJesawada/solar-power-mlops"
DEPLOYED_URL = "http://65.1.133.227:8501"


def ensure_assets_dir():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)


def draw_box(ax, xy, width, height, text, facecolor="#E8F0FE", edgecolor="#3367D6", fontsize=10):
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        linewidth=1.5,
        edgecolor=edgecolor,
        facecolor=facecolor,
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        weight="bold",
        wrap=True,
    )


def draw_arrow(ax, start, end, text=None):
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(arrowstyle="->", lw=1.8, color="#555555"),
    )
    if text:
        ax.text(
            (start[0] + end[0]) / 2,
            (start[1] + end[1]) / 2 + 0.02,
            text,
            fontsize=9,
            ha="center",
            va="center",
            color="#333333",
        )


def generate_architecture_diagram() -> Path:
    ensure_assets_dir()
    output = ASSETS_DIR / "system_architecture_diagram.png"
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    draw_box(ax, (0.05, 0.72), 0.2, 0.12, "Raw Data\nGeneration + Weather", "#FFF4E5", "#D97706")
    draw_box(ax, (0.33, 0.72), 0.2, 0.12, "DVC + AWS S3\nData Versioning", "#E8F5E9", "#2E7D32")
    draw_box(ax, (0.61, 0.72), 0.28, 0.12, "Data Ingestion + Preprocessing\nFeature Engineering", "#E3F2FD", "#1565C0")

    draw_box(ax, (0.1, 0.46), 0.22, 0.12, "Model Training\nXGBoost", "#F3E5F5", "#7B1FA2")
    draw_box(ax, (0.39, 0.46), 0.22, 0.12, "MLflow Tracking\nParams, Metrics, Artifacts", "#E0F7FA", "#00838F")
    draw_box(ax, (0.68, 0.46), 0.2, 0.12, "Evaluation + Monitoring\nPlots + Drift Report", "#FCE4EC", "#C2185B")

    draw_box(ax, (0.18, 0.2), 0.22, 0.12, "Streamlit App\nReal-time Prediction", "#E8F0FE", "#3367D6")
    draw_box(ax, (0.46, 0.2), 0.16, 0.12, "Docker", "#F1F8E9", "#558B2F")
    draw_box(ax, (0.68, 0.2), 0.2, 0.12, "AWS EC2\nCloud Deployment", "#FFF3E0", "#EF6C00")

    draw_arrow(ax, (0.25, 0.78), (0.33, 0.78))
    draw_arrow(ax, (0.53, 0.78), (0.61, 0.78))
    draw_arrow(ax, (0.5, 0.72), (0.21, 0.58))
    draw_arrow(ax, (0.61, 0.52), (0.61, 0.52))
    draw_arrow(ax, (0.43, 0.52), (0.39, 0.52))
    draw_arrow(ax, (0.61, 0.52), (0.68, 0.52))
    draw_arrow(ax, (0.21, 0.46), (0.28, 0.32))
    draw_arrow(ax, (0.5, 0.46), (0.54, 0.32))
    draw_arrow(ax, (0.79, 0.46), (0.79, 0.32))
    draw_arrow(ax, (0.4, 0.26), (0.46, 0.26))
    draw_arrow(ax, (0.62, 0.26), (0.68, 0.26))

    ax.text(0.5, 0.94, "System Architecture Diagram", ha="center", va="center", fontsize=16, weight="bold")
    fig.tight_layout()
    fig.savefig(output, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return output


def generate_pipeline_flow_diagram() -> Path:
    ensure_assets_dir()
    output = ASSETS_DIR / "pipeline_flow_diagram.png"
    fig, ax = plt.subplots(figsize=(8, 11))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    steps = [
        ("Data Versioning\n(DVC + S3)", "#E8F5E9", "#2E7D32"),
        ("data_ingestion.py", "#FFF4E5", "#D97706"),
        ("preprocessing.py", "#E3F2FD", "#1565C0"),
        ("train.py", "#F3E5F5", "#7B1FA2"),
        ("evaluate.py", "#FCE4EC", "#C2185B"),
        ("monitoring.py", "#E0F7FA", "#00838F"),
        ("app.py (Streamlit)", "#E8F0FE", "#3367D6"),
        ("Docker + EC2", "#FFF3E0", "#EF6C00"),
    ]

    y = 0.88
    for index, (label, fill, edge) in enumerate(steps):
        draw_box(ax, (0.25, y), 0.5, 0.08, label, fill, edge, fontsize=11)
        if index < len(steps) - 1:
            draw_arrow(ax, (0.5, y), (0.5, y - 0.06))
        y -= 0.12

    ax.text(0.5, 0.97, "End-to-End Pipeline Flow", ha="center", va="center", fontsize=16, weight="bold")
    fig.tight_layout()
    fig.savefig(output, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return output


def generate_methodology_diagram() -> Path:
    ensure_assets_dir()
    output = ASSETS_DIR / "methodology_diagram.png"
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    draw_box(ax, (0.05, 0.68), 0.25, 0.15, "Data Handling\nLoad, merge, clean,\ncreate time features", "#E3F2FD", "#1565C0")
    draw_box(ax, (0.375, 0.68), 0.25, 0.15, "Model Development\nTrain/test split,\nXGBoost training", "#F3E5F5", "#7B1FA2")
    draw_box(ax, (0.70, 0.68), 0.25, 0.15, "Experiment Strategy\nDVC + MLflow + params.yaml", "#E8F5E9", "#2E7D32")

    draw_box(ax, (0.12, 0.34), 0.22, 0.14, "Evaluation\nRMSE, MAE, R2,\nplots", "#FCE4EC", "#C2185B")
    draw_box(ax, (0.39, 0.34), 0.22, 0.14, "Monitoring\nDrift report,\npipeline logs", "#E0F7FA", "#00838F")
    draw_box(ax, (0.66, 0.34), 0.22, 0.14, "Deployment\nStreamlit, Docker,\nAWS EC2", "#FFF3E0", "#EF6C00")

    draw_arrow(ax, (0.30, 0.75), (0.375, 0.75))
    draw_arrow(ax, (0.625, 0.75), (0.70, 0.75))
    draw_arrow(ax, (0.175, 0.68), (0.23, 0.48))
    draw_arrow(ax, (0.50, 0.68), (0.50, 0.48))
    draw_arrow(ax, (0.825, 0.68), (0.77, 0.48))

    ax.text(0.5, 0.93, "Project Methodology Diagram", ha="center", va="center", fontsize=16, weight="bold")
    fig.tight_layout()
    fig.savefig(output, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return output


def add_page_number(section):
    footer = section.footer
    paragraph = footer.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = paragraph.add_run()
    fld_char1 = OxmlElement("w:fldChar")
    fld_char1.set(qn("w:fldCharType"), "begin")

    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = " PAGE "

    fld_char2 = OxmlElement("w:fldChar")
    fld_char2.set(qn("w:fldCharType"), "end")

    run._r.append(fld_char1)
    run._r.append(instr_text)
    run._r.append(fld_char2)


def set_base_style(document: Document):
    style = document.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    style.paragraph_format.space_after = Pt(6)
    style.paragraph_format.line_spacing = 1.15

    for name, size in [("Title", 20), ("Heading 1", 16), ("Heading 2", 14)]:
        style = document.styles[name]
        style.font.name = "Times New Roman"
        style.font.size = Pt(size)
        style.font.bold = True


def add_paragraph(document: Document, text: str, *, bold: bool = False, italic: bool = False):
    p = document.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    return p


def add_bullet(document: Document, text: str):
    document.add_paragraph(text, style="List Bullet")


def add_table(document: Document, headers, rows):
    table = document.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    for i, value in enumerate(headers):
        hdr[i].text = str(value)
        for paragraph in hdr[i].paragraphs:
            for run in paragraph.runs:
                run.bold = True
    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = str(value)
    return table


def add_image(document: Document, path: Path, caption: str, width: float = 5.8):
    if not path.exists():
        return
    p = document.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(path), width=Inches(width))
    cap = document.add_paragraph(caption)
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if cap.runs:
        cap.runs[0].italic = True


def add_section_heading(document: Document, title: str, level: int = 1):
    return document.add_heading(title, level=level)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def architecture_points():
    return [
        "Raw generation and weather datasets are tracked by DVC and stored remotely on AWS S3.",
        "The ingestion layer loads both datasets and validates their shapes before processing.",
        "The preprocessing layer merges the datasets on DATE_TIME, creates time-based features, and writes the processed file used for modeling.",
        "The training layer builds an XGBoost regression model and logs parameters plus model artifacts to MLflow.",
        "The evaluation layer computes RMSE, MAE, and R2 Score, and generates evaluation visualizations.",
        "The monitoring layer measures feature drift and generates drift reports for governance.",
        "The deployment layer exposes the trained model through Streamlit and Docker, and the application is hosted on AWS EC2.",
        "The CI/CD layer validates the end-to-end workflow through GitHub Actions by pulling DVC data, running the pipeline, and checking the app.",
    ]


def write_report():
    metrics = load_json(REPORTS_DIR / "metrics.json")
    drift = load_json(REPORTS_DIR / "drift_report.json")
    architecture_diagram = generate_architecture_diagram()
    pipeline_diagram = generate_pipeline_flow_diagram()
    methodology_diagram = generate_methodology_diagram()

    document = Document()
    set_base_style(document)

    section = document.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    add_page_number(section)

    title = document.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("Solar Power Generation Forecasting using an End-to-End MLOps Pipeline on AWS")
    run.bold = True
    run.font.size = Pt(20)
    run.font.name = "Times New Roman"

    for line in [
        "",
        "Student Names: _________________________________",
        "Roll Numbers: _________________________________",
        "Course Name: Essentials of MLOps",
        "Faculty Name: _________________________________",
        "",
        "Department of Artificial Intelligence and Machine Learning",
        "",
        "Academic Year: 2025-2026",
    ]:
        p = document.add_paragraph(line)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    document.add_page_break()

    add_section_heading(document, "Abstract")
    add_paragraph(
        document,
        "This project implements an end-to-end MLOps pipeline for forecasting solar power generation using weather and time-based features. "
        "The pipeline covers data versioning with DVC and AWS S3, experiment tracking with MLflow, modular training and evaluation, CI/CD with GitHub Actions, monitoring and governance, Docker containerization, and deployment on AWS EC2. "
        f"The final XGBoost regression model predicts AC_POWER and achieved RMSE {metrics['RMSE']}, MAE {metrics['MAE']}, and R2 Score {metrics['R2_Score']}. "
        "A Streamlit application was built for real-time inference, drift monitoring was implemented for governance, and the deployed Dockerized application was verified on an EC2 Ubuntu instance."
    )

    add_section_heading(document, "Introduction")
    add_section_heading(document, "Problem Statement", 2)
    add_paragraph(
        document,
        "Solar power generation is highly dependent on environmental conditions such as solar irradiation, ambient temperature, module temperature, and time of day. "
        "In renewable energy systems, forecasting the generated power is important for grid planning, energy management, and operational monitoring. "
        "This project addresses the problem of forecasting AC power generation from a solar plant using a machine learning model and an end-to-end MLOps pipeline."
    )
    add_section_heading(document, "Objectives", 2)
    for item in [
        "Develop a regression model to forecast solar AC power output.",
        "Build a modular and reproducible MLOps pipeline.",
        "Version raw data using DVC and store it in an AWS S3 remote.",
        "Track experiments, models, metrics, plots, and drift outputs using MLflow.",
        "Deploy the model as a real-time prediction application using Streamlit, Docker, and AWS EC2.",
        "Add CI/CD, monitoring, logging, and governance controls to improve reliability and maintainability.",
    ]:
        add_bullet(document, item)
    add_section_heading(document, "Scope of the Project", 2)
    add_paragraph(
        document,
        "The scope of this project includes raw data versioning, data preprocessing, model training, evaluation, monitoring, deployment, and governance documentation. "
        "The project focuses on a single plant dataset and a real-time prediction interface. It does not yet include HTTPS, automated production deployment, or advanced retraining orchestration."
    )

    add_section_heading(document, "Literature Review")
    add_paragraph(
        document,
        "Forecasting renewable energy output has become an important research area because energy generation from solar plants is inherently variable. "
        "Most practical solar forecasting systems rely on historical plant data, weather measurements, and temporal features. Supervised regression algorithms are widely applied because they can learn the relationship between environmental conditions and generated power."
    )
    add_paragraph(
        document,
        "Among tabular machine learning methods, gradient boosting models such as XGBoost are frequently used because they can capture nonlinear dependencies, interactions between features, and irregular patterns in operational data. "
        "At the same time, modern MLOps practices emphasize that a model alone is not sufficient. A full production-style workflow requires data versioning, experiment tracking, deployment readiness, monitoring, logging, and governance controls."
    )
    add_paragraph(
        document,
        "This project adopts that broader MLOps perspective by combining a forecasting model with DVC, MLflow, GitHub Actions, Docker, Streamlit, AWS S3, and AWS EC2. "
        "The result is not only a trained model but a complete pipeline that is reproducible, auditable, deployable, and easier to maintain."
    )

    add_section_heading(document, "System Architecture")
    add_section_heading(document, "Overall Architecture", 2)
    add_image(document, architecture_diagram, "Figure A. System Architecture Diagram", width=6.2)
    for point in architecture_points():
        add_bullet(document, point)
    add_paragraph(
        document,
        "The architecture separates responsibilities across data, modeling, experimentation, deployment, and governance. "
        "This separation makes the project easier to debug, extend, document, and evaluate against the Essentials of MLOps rubric."
    )

    add_section_heading(document, "Pipeline Flow")
    add_image(document, pipeline_diagram, "Figure B. End-to-End Pipeline Flow Diagram", width=5.5)
    add_paragraph(
        document,
        "The end-to-end pipeline begins with DVC-managed raw CSV files. The generation dataset and weather dataset are ingested, cleaned, merged, and transformed into a processed modeling dataset. "
        "The processed dataset is then used to train an XGBoost model, evaluate prediction quality, generate plots, and run drift checks. "
        "After training, the model is exposed through a Streamlit application for real-time prediction. The same project is validated in CI and containerized for deployment."
    )
    for step in [
        "Data collection and versioning",
        "Data ingestion",
        "Preprocessing and feature engineering",
        "Model training",
        "Evaluation and report generation",
        "Drift monitoring",
        "Real-time prediction interface",
        "Containerization and cloud deployment",
        "CI/CD validation and governance",
    ]:
        add_bullet(document, step)

    add_section_heading(document, "Tools and Technologies Used")
    add_table(
        document,
        ["Category", "Tools / Platforms", "Purpose"],
        [
            ["Programming", "Python", "Core implementation language"],
            ["Data Processing", "Pandas, NumPy", "Data loading, cleaning, merge, and feature handling"],
            ["Modeling", "XGBoost, Scikit-learn", "Regression and evaluation metrics"],
            ["Experiment Tracking", "MLflow", "Runs, parameters, metrics, model artifacts, drift artifacts"],
            ["Data Versioning", "DVC, AWS S3", "Raw data versioning and remote storage"],
            ["Visualization", "Matplotlib, Seaborn", "Exploratory and evaluation visualizations"],
            ["Deployment", "Streamlit, Docker, AWS EC2", "Real-time app, containerization, cloud hosting"],
            ["Automation", "GitHub Actions", "CI/CD validation workflow"],
            ["Governance and Logging", "Python logging, governance.md, Git", "Execution audit trail and process controls"],
        ],
    )

    add_section_heading(document, "Methodology")
    add_image(document, methodology_diagram, "Figure C. Methodology Diagram", width=6.2)
    add_section_heading(document, "Data Handling", 2)
    add_paragraph(
        document,
        "The project uses two raw datasets for Plant 1: generation data and weather sensor data. The generation data contains timestamped power and yield values, while the weather data contains irradiation and temperature measurements. "
        "During preprocessing, both datasets are aligned using DATE_TIME and merged into a single processed file."
    )
    add_paragraph(
        document,
        "The preprocessing stage converts timestamps, engineers HOUR, DAY, and MONTH features, removes null values, and writes the final dataset to data/processed/final_data.csv. "
        "Although the raw merged data contains other generation-related columns, the final forecasting model uses only weather and time features in order to avoid target leakage."
    )
    add_section_heading(document, "Model Development", 2)
    add_paragraph(
        document,
        "The target variable is AC_POWER. The model input features are AMBIENT_TEMPERATURE, MODULE_TEMPERATURE, IRRADIATION, HOUR, DAY, and MONTH. "
        "An XGBoost Regressor was selected because it performs strongly on structured tabular data and handles nonlinear relationships well."
    )
    add_paragraph(
        document,
        "The train-test split uses 80 percent training data and 20 percent testing data with random_state 42. Hyperparameters were configured through params.yaml so that the experiment remains reproducible and centrally configurable."
    )
    add_section_heading(document, "Versioning and Experimentation Strategy", 2)
    add_paragraph(
        document,
        "The project uses DVC to track raw data files and store them in an S3 remote. This ensures that raw data changes are reproducible and can be restored using dvc pull. "
        "MLflow is used to record experiment metadata, selected features, hyperparameters, train-test counts, model artifact, evaluation metrics, plots, and monitoring outputs."
    )

    add_section_heading(document, "Experiments and Results")
    add_section_heading(document, "Experimental Setup", 2)
    add_table(
        document,
        ["Item", "Value"],
        [
            ["Target Variable", "AC_POWER"],
            ["Features", "AMBIENT_TEMPERATURE, MODULE_TEMPERATURE, IRRADIATION, HOUR, DAY, MONTH"],
            ["Model", "XGBoost Regressor"],
            ["Test Size", "0.2"],
            ["Random State", "42"],
            ["n_estimators", "100"],
            ["max_depth", "6"],
            ["learning_rate", "0.1"],
        ],
    )
    add_section_heading(document, "Performance Metrics", 2)
    add_table(
        document,
        ["Metric", "Value", "Meaning"],
        [
            ["RMSE", metrics["RMSE"], "Root mean squared error"],
            ["MAE", metrics["MAE"], "Mean absolute error"],
            ["R2 Score", metrics["R2_Score"], "Explained variance score"],
        ],
    )
    add_paragraph(
        document,
        "The final model achieved a high R2 score while still relying only on weather and time features. This makes the forecasting setup more realistic than a model that uses generation-derived variables such as DC_POWER. "
        "Residual analysis and actual-versus-predicted plots show that the model captures the target trend effectively."
    )

    add_section_heading(document, "Result Visualizations", 2)
    for path, caption in [
        (REPORTS_DIR / "actual_vs_predicted.png", "Figure 1. Actual vs Predicted AC Power"),
        (REPORTS_DIR / "residual_distribution.png", "Figure 2. Residual Distribution"),
        (REPORTS_DIR / "residuals_vs_predicted.png", "Figure 3. Residuals vs Predicted AC Power"),
        (REPORTS_DIR / "evaluation_metrics.png", "Figure 4. Evaluation Metrics"),
        (REPORTS_DIR / "correlation_heatmap.png", "Figure 5. Feature Correlation Heatmap"),
        (REPORTS_DIR / "hourly_power.png", "Figure 6. Average Solar Power by Hour"),
    ]:
        add_image(document, path, caption)

    add_section_heading(document, "Comparative Study")
    add_paragraph(
        document,
        "An earlier intermediate version of the project used generation-related variables such as DC_POWER as inputs while predicting AC_POWER. Although that approach gave near-perfect results, it was not a strong forecasting design because those variables are too closely related to the target. "
        "The final model uses only weather and time-based features, which makes the prediction task more realistic, defensible, and suitable for demonstration in an MLOps context."
    )
    add_table(
        document,
        ["Approach", "Advantages", "Limitations"],
        [
            ["Leakage-prone feature set", "Artificially high scores", "Not suitable for realistic forecasting"],
            ["Final weather/time feature set", "Better reflects real deployment scenario", "Slightly harder prediction problem"],
            ["Implemented MLOps version", "Tracks data, experiments, deployment, and monitoring", "Future work can add automated retraining"],
        ],
    )

    add_section_heading(document, "Deployment")
    add_section_heading(document, "Deployment Strategy", 2)
    add_paragraph(
        document,
        "A real-time deployment approach was selected for this project. The user provides current weather and time values through the Streamlit interface, and the model immediately returns the predicted AC power value. "
        "This approach is appropriate because the use case is interactive forecasting rather than offline batch scoring."
    )
    add_section_heading(document, "Deployment Implementation", 2)
    add_paragraph(
        document,
        "The Streamlit application was containerized using Docker and deployed on an AWS EC2 Ubuntu instance. "
        "Docker provides environment consistency, while EC2 offers flexible cloud hosting for the containerized app. The EC2 security group was configured to allow inbound traffic on port 8501."
    )
    add_table(
        document,
        ["Deployment Item", "Value"],
        [
            ["Platform", "AWS EC2 (Ubuntu 22.04)"],
            ["Instance Type", "t3.micro"],
            ["Container Runtime", "Docker"],
            ["Application Port", "8501"],
            ["Public URL", DEPLOYED_URL],
        ],
    )

    add_section_heading(document, "Monitoring and Maintenance")
    add_paragraph(
        document,
        "The monitoring stage compares reference and current feature distributions and writes a JSON drift report. "
        f"The configured drift threshold is {drift['threshold_percent']} percent. The latest run reported drift_detected = {drift['drift_detected']}. "
        "These monitoring outputs are also logged to MLflow, making them visible in the experiment history."
    )
    add_table(
        document,
        ["Feature", "Reference Mean", "Current Mean", "Drift %", "Drift Detected"],
        [
            [
                feature,
                values["reference_mean"],
                values["current_mean"],
                values["drift_percent"],
                values["drift_detected"],
            ]
            for feature, values in drift["features"].items()
        ],
    )
    add_paragraph(
        document,
        "Maintenance strategy for the project includes checking logs in logs/pipeline.log, reviewing MLflow runs, observing drift behavior, and retraining the model if drift or performance degradation becomes significant."
    )

    add_section_heading(document, "Conclusion and Future Work")
    add_paragraph(
        document,
        "This project successfully demonstrates a complete MLOps workflow for solar power forecasting. It covers data versioning, modular pipeline design, experiment tracking, CI/CD, real-time deployment, monitoring, logging, governance, and cloud hosting. "
        "The final result is not just a machine learning model but a project that is reproducible, testable, deployable, and aligned with the Essentials of MLOps rubric."
    )
    add_paragraph(
        document,
        "Future work can include adding HTTPS and custom domain support for the deployed application, setting up automated deployment from GitHub Actions to AWS, introducing more advanced statistical drift detection, and implementing a retraining pipeline triggered by drift or performance decay."
    )

    add_section_heading(document, "References")
    for ref in [
        "[1] T. Chen and C. Guestrin, “XGBoost: A Scalable Tree Boosting System,” Proc. 22nd ACM SIGKDD Int. Conf. Knowledge Discovery and Data Mining, 2016, pp. 785-794.",
        "[2] MLflow, “MLflow Documentation.” [Online]. Available: https://mlflow.org/docs/latest/index.html",
        "[3] DVC, “Data Version Control Documentation.” [Online]. Available: https://dvc.org/doc",
        "[4] Docker, “Docker Documentation.” [Online]. Available: https://docs.docker.com/",
        "[5] Streamlit, “Streamlit Documentation.” [Online]. Available: https://docs.streamlit.io/",
        "[6] GitHub, “GitHub Actions Documentation.” [Online]. Available: https://docs.github.com/actions",
        "[7] Amazon Web Services, “Amazon EC2 Documentation.” [Online]. Available: https://docs.aws.amazon.com/ec2/",
    ]:
        add_paragraph(document, ref)

    add_section_heading(document, "GitHub Repository")
    add_paragraph(document, REPO_URL)
    add_paragraph(
        document,
        "The repository contains the full project implementation, including source code, pipeline modules, configuration files, DVC pointers, MLflow tracking outputs, governance documentation, CI workflow, Docker files, and deployment instructions."
    )

    add_section_heading(document, "Appendix: Suggested Screenshots for Final Submission")
    for item in [
        "GitHub repository home page",
        "GitHub Actions successful workflow run",
        "MLflow experiment UI showing the latest unified run",
        "Streamlit prediction app screenshot",
        "AWS S3 bucket used as the DVC remote",
        "AWS EC2 instance details",
        "EC2 security group inbound rules for port 8501",
        "Docker container running on EC2 (`docker ps` output)",
        "Drift report JSON file",
        "Pipeline log file (`logs/pipeline.log`)",
    ]:
        add_bullet(document, item)

    appendix = document.add_section(WD_SECTION.NEW_PAGE)
    add_page_number(appendix)

    document.save(OUTPUT)
    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    write_report()
