# Phase 3: ML Models - COMPLETE ✅

**Completion Date**: 2025-10-13  
**Status**: All sprints completed successfully

---

## Overview

Phase 3 delivered a complete machine learning pipeline with feature engineering, multiple model architectures (LSTM, XGBoost, RandomForest), MLflow experiment tracking, model serving infrastructure, and SHAP-based explainability.

---

## Sprints Completed

### Sprint 7: Feature Engineering & Dataset Preparation ✅
- Multi-source feature extraction (displacement, economic, conflict, climate)
- Time series features (lag, rolling windows, growth rates)
- Temporal train/val/test splits (prevents data leakage)
- Sequence creation for LSTM models
- Preprocessing artifacts (scalers, feature metadata)
- REST API for feature extraction

### Sprint 8: ML Model Training ✅
- LSTM model (2-layer with dropout)
- XGBoost model (gradient boosting)
- RandomForest model (baseline)
- MLflow experiment tracking
- Model registry (database storage)
- Model serving infrastructure
- Prediction storage and tracking

### Sprint 9: Model Explainability ✅
- SHAP explainability for tree models
- Global feature importance
- Single prediction explanations
- Waterfall and summary plots
- Native feature importance extraction
- Prediction confidence intervals (bootstrap)

---

## Architecture

### ML Pipeline Flow
```
Data Sources → Feature Engineering → Dataset Prep → Model Training → Serving
     ↓              ↓                    ↓               ↓            ↓
  Curated       Lag/Rolling         Temporal        LSTM/XGB      REST API
   Layer        Growth rates         splits         RF models    + caching
                Aggregations        Sequences       MLflow       + SHAP
```

### Model Types

**1. LSTM (Deep Learning)**
- 2-layer LSTM with dropout (0.2)
- Sequence length: 12 time steps
- Adam optimizer, MSE loss
- Early stopping + learning rate reduction
- Best for: Time series with temporal dependencies

**2. XGBoost (Gradient Boosting)**
- 100 trees, max depth 6
- Learning rate: 0.1
- Subsample: 0.8, colsample: 0.8
- Early stopping on validation
- Best for: Tabular data with complex interactions

**3. Random Forest (Baseline)**
- 100 trees, unlimited depth
- Parallel training
- Feature importance
- Best for: Baseline comparison, interpretability

---

## Feature Engineering

### Displacement Features
- **Base**: refugees, asylum_seekers, idps, returnees, stateless, total_displaced
- **Lag**: 1, 3, 12 periods
- **Rolling**: 3 and 12-period mean/std
- **Growth**: Period-over-period % change

### Economic Features
- **Indicators**: GDP, poverty, unemployment, inflation, etc.
- **Transformations**: Lag, % change
- **Format**: Pivoted wide format

### Conflict Features
- **Aggregations**: Event counts by type, total fatalities
- **Temporal**: Monthly aggregation
- **Spatial**: Country-level

### Climate Features
- **Measurements**: Temperature, precipitation, humidity, wind
- **Anomalies**: Deviation from historical mean
- **Spatial**: 0.5° grid matching

---

## MLflow Tracking

**Logged Parameters**:
- Model type and hyperparameters
- Sequence length (LSTM)
- Number of features
- Training configuration

**Logged Metrics**:
- Training/validation loss per epoch
- Test RMSE, MAE, R²
- Feature importance (top 10)

**Logged Artifacts**:
- Trained model files
- Preprocessing scalers
- Training history

---

## Model Serving

### Database Tables

**ml_models**:
- Model metadata (name, type, version)
- Training info (dates, features, hyperparameters)
- Performance metrics (RMSE, MAE, R²)
- MLflow tracking IDs
- File paths (model, scaler)
- Status and active flag

**predictions**:
- Model ID reference
- Country and prediction date
- Predicted value
- Confidence intervals
- Actual value (for evaluation)
- Input features

### Serving Features
- **Model caching**: In-memory cache for loaded models
- **Active model management**: Deploy/undeploy models
- **Batch predictions**: Efficient bulk inference
- **Prediction storage**: Track all predictions in database

---

## Explainability

### SHAP (SHapley Additive exPlanations)
- **Global explanations**: Feature importance across dataset
- **Local explanations**: Single prediction breakdown
- **Visualizations**: Summary plots, waterfall plots (base64 encoded)
- **Supported models**: XGBoost, RandomForest

### Feature Importance
- **Native importance**: From tree-based models
- **SHAP values**: Mean absolute SHAP across samples
- **Top features**: Ranked by importance

### Confidence Intervals
- **Bootstrap method**: 100 iterations
- **Intervals**: 90% and 95% confidence
- **Metrics**: Mean, std, lower/upper bounds

---

## REST API Endpoints

### Feature Extraction (`/api/v1/ml/features`)
- `POST /displacement` - Displacement features
- `POST /economic` - Economic features
- `POST /conflict` - Conflict features

### Dataset Creation (`/api/v1/ml/dataset`)
- `POST /create` - Complete ML dataset

### Predictions (`/api/v1/ml`)
- `POST /predict` - Make prediction
- `GET /models` - List models
- `GET /models/{id}` - Get model info
- `POST /models/activate` - Activate model

### Explainability (`/api/v1/ml/explain`)
- `POST /global` - Global SHAP explanation
- `POST /single` - Single prediction explanation
- `GET /models/{id}/feature-importance` - Feature importance

---

## API Examples

### Extract Features
```bash
curl -X POST http://localhost:8000/api/v1/ml/features/displacement \
  -H "Content-Type: application/json" \
  -d '{"country_iso": "AFG", "start_date": "2015-01-01", "end_date": "2023-12-31"}'
```

### Create ML Dataset
```bash
curl -X POST http://localhost:8000/api/v1/ml/dataset/create \
  -H "Content-Type: application/json" \
  -d '{
    "country_iso": "AFG",
    "start_date": "2015-01-01",
    "end_date": "2023-12-31",
    "latitude": 33.9,
    "longitude": 67.7
  }'
```

### Make Prediction
```bash
curl -X POST http://localhost:8000/api/v1/ml/predict \
  -H "Content-Type: application/json" \
  -d '{
    "model_type": "XGBoost",
    "features": [[100, 50, 25, 10, 5, 1.5, 2.3]],
    "country_iso": "AFG"
  }'
```

### Get SHAP Explanation
```bash
curl -X POST http://localhost:8000/api/v1/ml/explain/global \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": 5,
    "features": [[100, 50, 25], [120, 55, 30]],
    "feature_names": ["refugees", "gdp", "conflicts"],
    "max_display": 10
  }'
```

---

## Files Created

### ML Package
- `app/ml/__init__.py` - Package init
- `app/ml/features.py` - Feature engineering (400+ lines)
- `app/ml/dataset.py` - Dataset preparation (300+ lines)
- `app/ml/models.py` - Model classes (400+ lines)
- `app/ml/training.py` - Training orchestration (250+ lines)
- `app/ml/serving.py` - Model serving (300+ lines)
- `app/ml/explainability.py` - SHAP explainability (350+ lines)

### Database
- `app/models/ml_models.py` - ML model tables
- `alembic/versions/005_ml_models.py` - Migration

### API
- `app/api/ml.py` - ML REST endpoints (450+ lines)

### Updates
- `app/main.py` - Added ML router, version 0.4.0
- `requirements.txt` - Added ML dependencies

---

## Dependencies Added

```
scikit-learn>=1.3,<2      # ML models and preprocessing
tensorflow>=2.14,<3        # Deep learning (LSTM)
xgboost>=2.0,<3           # Gradient boosting
shap>=0.43,<1             # Model explainability
matplotlib>=3.7,<4        # Plotting for SHAP
mlflow>=2.8,<3            # Experiment tracking
joblib>=1.3,<2            # Model serialization
numpy>=1.24,<2            # Numerical computing
pandas>=2.0,<3            # Data manipulation
```

---

## Key Achievements

✅ **Feature Engineering**: Multi-source, time series, spatial  
✅ **3 Model Types**: LSTM, XGBoost, RandomForest  
✅ **MLflow Integration**: Full experiment tracking  
✅ **Model Registry**: Database storage with metadata  
✅ **Model Serving**: REST API with caching  
✅ **SHAP Explainability**: Global and local explanations  
✅ **Prediction Tracking**: All predictions stored  
✅ **Data Leakage Prevention**: Temporal splits, scaler fit on train  
✅ **Confidence Intervals**: Bootstrap-based uncertainty  
✅ **Feature Importance**: Native and SHAP-based  

---

## Performance Metrics

Models evaluated on:
- **RMSE** (Root Mean Squared Error)
- **MAE** (Mean Absolute Error)
- **R²** (Coefficient of Determination)

All metrics logged to MLflow and stored in database.

---

## Next Steps (Phase 4)

- ⏳ React frontend application
- ⏳ Interactive map with Mapbox/Leaflet
- ⏳ Time series charts with Recharts
- ⏳ Model comparison dashboard
- ⏳ Data source explorer
- ⏳ Report builder

---

## Verification Commands

### Run Migrations
```bash
cd backend
alembic upgrade head
```

### Start API
```bash
uvicorn app.main:app --reload
```

### Train Models (Python)
```python
from app.ml.training import ModelTrainer
from app.ml.dataset import DatasetPreparation

# Prepare dataset
prep = DatasetPreparation()
dataset = prep.prepare_tabular_dataset(df, target_column="total_displaced")

# Train models
trainer = ModelTrainer(experiment_name="migration_forecasting")
xgb_result = trainer.train_xgboost(dataset)
rf_result = trainer.train_random_forest(dataset)

# Compare
comparison = trainer.compare_models(lstm_result, xgb_result, rf_result)
```

### View MLflow UI
```bash
mlflow ui
# Navigate to http://localhost:5000
```

---

**Phase 3 Status**: ✅ COMPLETE  
**Ready for Phase 4**: ✅ YES  
**Version**: 0.4.0  
**Total Lines of ML Code**: ~2,500+
