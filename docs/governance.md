# MLOps Governance

This document summarizes how the project handles data, model, code, logging,
monitoring, and deployment governance.

## Data Governance

Raw datasets are versioned with DVC and stored remotely in AWS S3.

Remote:

```text
s3://solar-mlops-data-abizer/dvcstore
```

Governance controls:

- Raw data is not manually overwritten in Git.
- DVC pointer files track dataset versions.
- `dvc pull` restores the exact data version needed by the pipeline.
- GitHub Actions validates that DVC data can be pulled from the S3 remote.

## Experiment Governance

MLflow is used for experiment tracking.

Tracked items:

- Model target
- Input features
- Hyperparameters
- Train/test sample counts
- Model artifact
- Evaluation metrics
- Evaluation plots
- Drift metrics
- Drift report artifact

This makes each training run auditable and reproducible.

## Model Governance

The model predicts:

```text
AC_POWER
```

Only weather and time features are used for forecasting:

```text
AMBIENT_TEMPERATURE
MODULE_TEMPERATURE
IRRADIATION
HOUR
DAY
MONTH
```

This avoids target leakage from generation columns such as `DC_POWER`.

Model artifact:

```text
models/model.pkl
```

## Monitoring Governance

Data drift monitoring is implemented in:

```text
src/pipeline/monitoring.py
```

The monitoring step compares the first 80% of processed records as reference
data against the latest 20% as current data.

Output:

```text
reports/drift_report.json
```

The drift threshold is configured in:

```text
params.yaml
```

Current threshold:

```text
20 percent
```

If drift exceeds the threshold, the model should be reviewed and retraining
should be considered.

## Logging Governance

Pipeline execution logs are written to:

```text
logs/pipeline.log
```

The log captures:

- Pipeline start and completion
- Data ingestion shapes
- Preprocessing output shape
- Training sample counts
- Evaluation metrics
- Drift status

The `logs/` directory is ignored by Git because logs are runtime artifacts.

## Code Governance

Code changes are managed with Git and GitHub.

Controls:

- Git commits record project history.
- GitHub Actions runs CI on pushes to `main`.
- CI validates syntax, pulls DVC data, runs the ML pipeline, validates the app,
  and uploads model/report artifacts.

Workflow:

```text
.github/workflows/ci.yml
```

## Deployment Governance

The Streamlit app is containerized with Docker.

Deployment files:

```text
Dockerfile
.dockerignore
docker-requirements.txt
```

The Docker image can be deployed to AWS services such as ECS, EC2, App Runner,
or an ECR-based deployment workflow.

## Security Notes

- AWS credentials must not be committed to Git.
- AWS credentials are stored as GitHub repository secrets for CI.
- `.env` files are ignored by Git.
- DVC remote access should use least-privilege IAM permissions where possible.
