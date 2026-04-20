# Solar Power Generation Forecasting using MLOps

This project builds an end-to-end machine learning pipeline to forecast solar
power generation from weather and time-based features. The pipeline uses DVC for
data versioning, MLflow for experiment tracking, XGBoost for regression,
GitHub Actions for CI, and Streamlit for an interactive prediction interface.

## Problem Statement

Solar power generation changes with environmental conditions such as
irradiation, ambient temperature, module temperature, and time of day. The goal
of this project is to predict the plant's AC power output so that solar energy
generation can be monitored and forecasted more effectively.

This is a supervised regression problem.

Target variable:

```text
AC_POWER
```

Input features:

```text
AMBIENT_TEMPERATURE
MODULE_TEMPERATURE
IRRADIATION
HOUR
DAY
MONTH
```

## Tech Stack

- Python
- Pandas and NumPy
- Scikit-learn
- XGBoost
- DVC with AWS S3 remote
- MLflow
- Matplotlib and Seaborn
- Streamlit
- GitHub Actions
- Git and GitHub

## Project Structure

```text
solar-power-mlops/
|-- app.py
|-- main.py
|-- params.yaml
|-- requirements.txt
|-- .github/workflows/ci.yml
|-- data/
|   |-- raw/
|   |   |-- Plant_1_Generation_Data.csv.dvc
|   |   `-- Plant_1_Weather_Sensor_Data.csv.dvc
|   `-- processed/
|       `-- final_data.csv
|-- models/
|   `-- model.pkl
|-- reports/
|   |-- metrics.json
|   |-- drift_report.json
|   |-- actual_vs_predicted.png
|   |-- residual_distribution.png
|   |-- residuals_vs_predicted.png
|   `-- evaluation_metrics.png
`-- src/
    `-- pipeline/
        |-- data_ingestion.py
        |-- preprocessing.py
        |-- train.py
        |-- evaluate.py
        |-- monitoring.py
        `-- visualization.py
```

## Pipeline Flow

1. `data_ingestion.py` loads raw generation and weather datasets.
2. `preprocessing.py` merges datasets, parses timestamps, creates time features,
   and saves processed data.
3. `train.py` trains an XGBoost regression model and logs parameters/model to
   MLflow.
4. `evaluate.py` calculates metrics, saves evaluation plots, and logs metrics
   and artifacts to MLflow.
5. `monitoring.py` creates a drift report by comparing reference and current
   feature distributions.
6. `app.py` provides a Streamlit interface for real-time prediction.

Run the complete pipeline:

```powershell
python main.py
```

## Data Versioning with DVC

The raw CSV files are tracked using DVC. The DVC remote is configured on AWS S3:

```text
s3://solar-mlops-data-abizer/dvcstore
```

Pull data from DVC remote:

```powershell
dvc pull
```

Check DVC status:

```powershell
dvc status
```

## Experiment Tracking with MLflow

MLflow tracks:

- Model parameters
- Selected features
- Target column
- Trained model artifact
- Evaluation metrics
- Evaluation plots

Start the MLflow UI:

```powershell
mlflow ui --port 5001
```

Open:

```text
http://127.0.0.1:5001
```

Experiment name:

```text
solar-power-forecasting
```

## Model Results

Current model:

```text
XGBoost Regressor
```

Latest evaluation metrics:

```json
{
  "RMSE": 45.8368,
  "MAE": 16.9224,
  "R2_Score": 0.9864
}
```

The model forecasts `AC_POWER` using only weather and time features. This is
more realistic than using generation columns such as `DC_POWER`, because those
are directly related to the target.

## Streamlit Prediction App

Run the app:

```powershell
python -m streamlit run app.py
```

Open:

```text
http://localhost:8501
```

The app accepts weather and time inputs and returns:

```text
Predicted AC Power
```

## Monitoring and Drift Detection

The project includes a simple data drift monitoring step in
`src/pipeline/monitoring.py`. It compares the first 80% of processed records as
reference data against the latest 20% as current data.

For each model feature, it calculates:

- Reference mean
- Current mean
- Percentage drift
- Drift detected flag

The drift threshold is configured in `params.yaml`:

```yaml
monitoring:
  drift_threshold_percent: 20
```

Run monitoring as part of the full pipeline:

```powershell
python main.py
```

Or run only monitoring:

```powershell
python src/pipeline/monitoring.py
```

Output:

```text
reports/drift_report.json
```

## CI/CD with GitHub Actions

The project uses GitHub Actions for CI. On each push to `main`, the workflow:

- Sets up Python
- Installs required ML and MLOps dependencies
- Pulls DVC-tracked data from AWS S3
- Runs the training and evaluation pipeline
- Validates the Streamlit app import
- Uploads generated model and report artifacts

Workflow file:

```text
.github/workflows/ci.yml
```

## Visualizations

Evaluation plots:

- `reports/actual_vs_predicted.png`
- `reports/residual_distribution.png`
- `reports/residuals_vs_predicted.png`
- `reports/evaluation_metrics.png`

Dataset exploration plots:

- `reports/ac_power_distribution.png`
- `reports/irradiation_vs_power.png`
- `reports/temperature_vs_power.png`
- `reports/hourly_power.png`
- `reports/correlation_heatmap.png`

Generate exploratory plots:

```powershell
python src/pipeline/visualization.py
```

## Reproducibility

Create and activate a virtual environment:

```powershell
python -m venv mlops
.\mlops\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the pipeline:

```powershell
python main.py
```

Run the app:

```powershell
python -m streamlit run app.py
```

## Rubric Mapping

| Rubric Criteria | Project Coverage |
| --- | --- |
| Problem Definition & ML Use Case | Solar AC power forecasting regression problem |
| Data Versioning & Experiment Tracking | DVC with S3 remote, MLflow experiment tracking |
| Modular Pipeline Design | Separate ingestion, preprocessing, training, evaluation, monitoring, visualization modules |
| CI/CD Implementation | GitHub Actions runs DVC pull, training, evaluation, app validation, and artifact upload |
| Model Deployment Strategy | Streamlit prediction app for real-time demo |
| Cloud Deployment & Infrastructure | AWS S3 used for DVC remote and Docker assets are ready for container deployment |
| Monitoring, Logging & Governance | MLflow logging, pipeline logs, drift report, and governance document implemented |
| GitHub Repository & Reproducibility | Git repo, requirements, DVC pointers, pipeline commands |
| Technical Project Report | This README provides base material for report |

## Pipeline Logging

The project uses Python logging for pipeline execution logs. Logs are written to:

```text
logs/pipeline.log
```

The log file records data ingestion, preprocessing, training, evaluation,
monitoring, metrics, and drift status. The `logs/` directory is ignored by Git.

## Governance

Project governance is documented in:

```text
docs/governance.md
```

It covers data governance, experiment tracking, model governance, monitoring,
logging, CI/CD controls, deployment governance, and security notes.

## Docker Deployment

The Streamlit app is containerized for deployment readiness.

Files:

```text
Dockerfile
.dockerignore
docker-requirements.txt
```

Build the image:

```powershell
docker build -t solar-power-mlops .
```

Run the container:

```powershell
docker run -p 8501:8501 solar-power-mlops
```

Open:

```text
http://localhost:8501
```

This containerization makes the project easier to deploy on AWS services such
as ECS, EC2, App Runner, or ECR-based workflows.

## Future Work

- Deploy the app on AWS.
- Improve experiment organization so training parameters and evaluation metrics
  are logged in a single MLflow run.
