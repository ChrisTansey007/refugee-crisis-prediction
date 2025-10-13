# Phase 3 Plan — ML Model Implementation (Sprints 7–9)
 
 Last Updated: 2025-10-13
Owner: ML Lead
Cross-Refs: IMPLEMENTATION_GUIDE.md (Phase 3), ARCHITECTURE.md (ML Pipeline), DATA_SOURCES.md (features), UI_DESIGN.md (explainability), DEPLOYMENT.md (serving/metrics)
 
## Required Reference Docs
 
- [README.md](./README.md)
- [PROJECT_PLAN.md](./PROJECT_PLAN.md)
- [DEVELOPMENT_READINESS.md](./DEVELOPMENT_READINESS.md)
- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [DATA_SOURCES.md](./DATA_SOURCES.md)
- [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)
- [UI_DESIGN.md](./UI_DESIGN.md)
- [DEPLOYMENT_RENDER.md](./DEPLOYMENT_RENDER.md)
- [render.yaml](./render.yaml)
- [DEPLOYMENT.md](./DEPLOYMENT.md) (optional)
 
---
 
## Phase Goals
- Assemble reproducible feature datasets from curated tables
- Train baseline models (classical + LSTM) with solid evaluation
- Implement explainability (SHAP) and uncertainty bands
- Package and serve predictions via FastAPI with basic monitoring
- No large-scale hyperparameter tuning (basic Optuna only)
- No complex ensembles beyond initial baseline (advanced in Phase 5 optional)

---

## Sprint 7 (Week 13–14): Feature Engineering & Datasets

### Objectives
- Define target variable(s) and assemble feature matrix from curated layer
- Implement dataset versioning and experiment tracking

### Tasks (Step-by-Step for Junior Dev)
- Targets & Windows
  - Define prediction horizon(s): 4, 8, 12, 26 weeks ahead
  - Compute rolling aggregates and lag features per region
  - Ensure leakage prevention (use only past data for each target window)
- Feature Assembly
  - Source features from `fact_displacement`, `fact_conflict`, `fact_climate`, `fact_economic`
  - Aggregate to monthly cadence for initial baseline
  - Create `features_{daily|monthly}` materialized views (if not yet present)
- Dataset Splits
  - Temporal split: Train (<= 2022), Val (2023), Test (2024-)
  - Save split indices to repository (`data/splits/`)
- Experiment Tracking
  - Add lightweight tracking (CSV/JSON logs). Optionally W&B or MLflow later
  - Record params, metrics, dataset hash/checksum
- Data Loaders
  - Build PyTorch-friendly `Dataset` for LSTM; pandas DataFrame for classical models
  - Normalize features; persist scalers

### Acceptance Criteria
- Reproducible dataset build script with CLI (e.g., `python -m app.ml.build_dataset`)
- Split artifacts saved; checksum logged; data catalog entry updated
- Feature importance sanity check produced for classical model (stub)

### Deliverables
- Dataset build scripts + docs
- Feature lists with definitions and data lineage
- Baseline EDA notebook (optional) with plots

### Demo Script
- Run dataset build; show train/val/test sizes
- Display example feature rows; confirm no leakage via date checks

---

## Sprint 8 (Week 15–16): Baseline Models & Evaluation

### Objectives
- Train classical baselines and an LSTM baseline; compute metrics and save artifacts

### Tasks
- Baseline Models
  - Classical: Linear Regression, RandomForest, XGBoost on monthly features
  - Neural: LSTM (univariate and small multivariate) with simple architecture
- Evaluation
  - Metrics: MAE, RMSE overall and per region; MAPE where defined
  - Backtesting with rolling-origin evaluation (time-aware CV)
  - Calibration: simple prediction intervals via residuals/quantiles
- Model Artifacts
  - Save model binaries, scalers, feature lists to `data/models/`
  - Generate evaluation reports (JSON + HTML summary)
- Reproducibility
  - Seed control; deterministic options where possible
  - Config files (`configs/model_*.yaml`) for parameters

### Acceptance Criteria
- At least two classical models and one LSTM trained with metrics logged
- Artifacts saved with versioned directory names (timestamp or git SHA)
- Evaluation report includes per-region breakdown and error histograms

### Deliverables
- Models + scalers + config files
- Evaluation report(s) checked into `data/reports/`

### Demo Script
- Show training command(s) and completion
- Open report summarizing metrics and sample predictions

---

## Sprint 9 (Week 17–18): Serving, Explainability & Monitoring

### Objectives
- Serve predictions via FastAPI; compute SHAP explanations; add basic monitoring

### Tasks
- Serving API (FastAPI)
  - Endpoint: `POST /api/v1/predictions` with body: region_id(s), horizon, date
  - Response: predictions, intervals, model metadata, feature set version
  - Health: `/api/v1/models` to list available versions
- Explainability
  - SHAP summary for selected region/time window (cached)
  - Expose `GET /api/v1/explain?region_id=...&date=...` returning top features
- Caching & Performance
  - Redis cache for repeated requests (keyed by params)
  - Batch request support for multiple regions
- Monitoring
  - Prometheus metrics: request count, latency, model version tag
  - Accuracy drift placeholder: schedule offline job to compare recent preds vs. actuals

### Acceptance Criteria
- Prediction endpoint returns values with confidence bands within <500ms for 1 region
- Explain endpoint returns SHAP top-k features; cached responses observed
- Metrics exposed at `/metrics` with model labels

### Deliverables
- Serving layer integrated with trained artifacts
- SHAP computation utilities and cache
- Monitoring hooks + Grafana panel JSON (optional)

### Demo Script
- Call `/predictions` for a sample region and display output
- Call `/explain` and show top features and SHAP summary chart (API returns data)

---

## Roles & Estimates
- ML Engineer: 70%
- Backend Dev: 20% (serving endpoints)
- DevOps: 10% (metrics exposure)

---

## Exit Criteria (Phase Gate)
- Reproducible datasets and splits
- Baseline models trained with reports and saved artifacts
- Prediction + explainability endpoints operational with monitoring
