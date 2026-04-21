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
- Docker
- AWS EC2
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

## Automated EC2 Deployment

The repository also includes a deployment workflow that can redeploy the
Dockerized Streamlit app to an EC2 instance whenever code is pushed to `main`.

Workflow file:

```text
.github/workflows/deploy-ec2.yml
```

Required GitHub repository secrets:

```text
EC2_HOST
EC2_USER
EC2_SSH_PRIVATE_KEY
```

Deployment behavior:

- Connects to the EC2 instance over SSH
- Clones the repository if it is not already present
- Fetches the latest `main` branch state
- Rebuilds the Docker image
- Recreates the `solar-app` container on port `8501`

This keeps the deployed Streamlit dashboard aligned with the latest GitHub
changes after each push to `main`.

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
| Cloud Deployment & Infrastructure | AWS S3 used for DVC remote and Dockerized Streamlit app deployed on AWS EC2 |
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

## AWS EC2 Deployment

The Streamlit prediction app was deployed on an AWS EC2 Ubuntu instance using
Docker.

Deployment summary:

```text
Streamlit app -> Docker image -> Docker container -> AWS EC2 -> Public URL
```

EC2 setup:

```text
AMI: Ubuntu 22.04
Instance type: t3.micro
Application port: 8501
Security group inbound rule: Custom TCP 8501 from 0.0.0.0/0
```

Commands used on EC2:

```bash
sudo apt update
sudo apt install -y docker.io git
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
git clone https://github.com/AbizerJesawada/solar-power-mlops.git
cd solar-power-mlops
docker build -t solar-power-mlops .
docker run -d -p 8501:8501 --name solar-app solar-power-mlops
docker ps
```

If you enable the deployment workflow, GitHub Actions can perform the update
steps automatically after pushes to `main`, so the EC2 instance stays in sync
with the repository without a manual SSH session.

Deployed app URL:

```text
http://65.1.133.227:8501
```

Note: The EC2 instance should be stopped when not in use to avoid unnecessary
AWS charges.

## Future Work

- Add HTTPS/domain support for the deployed app.
- Add automated deployment from GitHub Actions to AWS.
