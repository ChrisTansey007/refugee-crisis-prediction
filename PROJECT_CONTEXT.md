# PROJECT_CONTEXT.md

## Purpose

This file holds durable context learned after ROWS is installed into this repository.

Use it for:

- recurring constraints
- durable assumptions
- architecture context that is not formal enough for an ADR
- distilled lessons from handoffs

Do not use it for:

- raw command logs
- temporary session narration
- work that already lives in active task files or blockers

## Current Project State

Describe the current stable state of the project in 2-5 bullets.

## Durable Facts

- [Add facts that future workers should not need to rediscover]

## Active Constraints

- [Runtime, product, team, compliance, or repo constraints]

## Decisions and ADR Cross-References

- [Link important decisions and explain why they matter]

## Assumptions Being Carried

- [List assumptions still shaping active work]

## Known Risks and Watch Items

- [List continuing risks]

## Agent Operating Notes

- [Anything future workers should know before reading raw handoffs]

## Recently Distilled Handoffs

- none yet

## Open Context Questions

- [What still needs clarification]


## Expert-Level Tasks Added (via ROWS System)
On 2026-05-11 18:35:39, ten expert-level tasks were created to advance the refugee crisis prediction system toward production readiness:

- TASK-0017: implement-hyperparameter-tuning-for-lstm (ML Engineer)
- TASK-0018: design-explainable-ai-ui-for-predictions (Frontend Engineer / ML Engineer)
- TASK-0019: implement-chaos-testing-for-data-pipeline (DevOps Engineer)
- TASK-0020: build-data-lineage-tracking-system (Data Engineer)
- TASK-0021: optimize-model-serving-with-tensorrt (ML Engineer / DevOps Engineer)
- TASK-0022: implement-federated-learning-for-regional-models (ML Engineer)
- TASK-0023: build-real-time-prediction-api-with-websockets (Backend Engineer / Frontend Engineer)
- TASK-0024: implement-advanced-feature-engineering-pipeline (Data Engineer / ML Engineer)
- TASK-0025: design-multi-modal-fusion-architecture (ML Engineer / Data Scientist)
- TASK-0026: implement-automated-model-retraining-trigger (ML Engineer / DevOps Engineer)

These tasks focus on:
- Advanced ML techniques (hyperparameter tuning, explainable AI, federated learning)
- System resilience and observability (chaos testing, data lineage, monitoring)
- Performance optimization (TensorRT, real-time APIs, feature engineering)
- Future enhancements (multi-modal fusion, automated retraining)


## Durable Knowledge: TASK-0017 Completion
**Completed**: 2026-05-11 18:46:29
**Task**: TASK-0017-implement-hyperparameter-tuning-for-lstm
**Expert Role**: ML Engineer
**Summary**: Successfully implemented automated hyperparameter tuning for LSTM migration forecasting model using Optuna optimization framework.

**Key Implementation Details**:
- Created LSTMHyperparameterTuner class with comprehensive search space for LSTM hyperparameters
- Implemented LSTMTrainingService for model training, validation, and checkpointing
- Integrated Optuna with TPE sampler and Median pruner for efficient optimization
- Defined objective function minimizing validation RMSE with pruning capability
- Built gradient clipping, device handling (CPU/GPU), and proper error handling
- Designed for integration with existing MLModel and Prediction database tables
- Created verification evidence and handoff documentation per ROWS standards

**Files Created**:
- /app/ml/lstm_hyperparameter_tuner.py
- /app/services/training_service.py

**Next Steps Enabled**:
- Integration with data ingestion pipeline for automated model optimization
- MLflow experiment tracking for hyperparameter studies
- Automated retraining pipelines based on optimization results
- Extension to other model types (XGBoost, RandomForest, etc.)

**Impact**: This implementation enables the refugee crisis prediction system to automatically optimize its LSTM models for better forecasting accuracy, reducing manual tuning effort and improving model performance over time.


## Durable Knowledge: TASK-0018 Completion
**Completed**: 2026-05-11 19:06:20
**Task**: TASK-0018-design-explainable-ai-ui-for-predictions
**Expert Role**: Frontend Engineer / ML Engineer
**Summary**: Successfully designed and implemented explainable AI UI components for displaying SHAP and LIME explanations of model predictions in the refugee crisis prediction system.

**Key Implementation Details**:
- Created SHAPExplanation component with feature importance bar chart visualization
- Created LIMEExplanation component showing feature contributions as pie chart with prediction breakdown
- Built ExplanationContainer for tabbed navigation between explanation types
- Integrated all components into the Predictions page below existing charts and details
- Used existing UI libraries (Recharts, lucide-react) and followed Tailwind CSS styling conventions
- Implemented proper loading and error states
- Designed for connection to backend explanation API endpoints

**Files Created**:
- /frontend/src/components/explanation/SHAPExplanation.jsx
- /frontend/src/components/explanation/LIMEExplanation.jsx
- /frontend/src/components/explanation/ExplanationContainer.jsx
- /frontend/src/components/explanation/index.jsx

**Files Modified**:
- /frontend/src/pages/Predictions.jsx (added explanation components and imports)

**Next Steps Enabled**:
- Connection to real model explanation APIs for live SHAP/LIME values
- Model selection dropdown to choose which active model to explain
- Enhanced loading states and error handling
- Explanation history or comparison features
- Extension to other explanation methods (Integrated Gradients, etc.)

**Impact**: This implementation makes the refugee crisis prediction system's models transparent and interpretable, allowing stakeholders to understand why predictions are made and building trust in the AI system's recommendations.


## Durable Knowledge: TASK-0003 Completion
**Completed**: 2026-05-11 19:21:37
**Task**: TASK-0003-ingest-world-bank-data
**Expert Role**: Data Engineer
**Summary**: Successfully implemented automated extraction, transformation, and loading of World Bank economic indicators data for the refugee crisis prediction system.

**Key Implementation Details**:
- Verified World Bank connector works correctly with live API calls (tested GDP per capita for Somalia)
- Created ingestion script (ingest_worldbank.py) that uses existing IngestService framework
- Confirmed existing World Bank ingestion logic in IngestService is complete and handles multiple countries/indicators
- Verified staging table for World Bank data exists (StagingEconomic) with appropriate schema
- Implementation follows same proven pattern as UNHCR data ingestion

**Files Created**:
- /ingest_worldbank.py (main execution script)

**Files Verified/Reviewed**:
- /backend/app/connectors/worldbank.py (World Bank connector)
- /backend/app/services/ingest_service.py (ingestion orchestration service)
- /backend/app/models/data_ingest.py (data models including StagingEconomic)

**Next Steps Enabled**:
- Environment setup and end-to-end testing with database connection
- Scheduled automated runs for regular data updates
- Extension to additional World Bank indicators as needed
- Integration with economic features in migration forecasting models

**Impact**: This implementation adds crucial economic indicators (GDP, poverty, unemployment, inflation, etc.) to the refugee crisis prediction system, enabling models to incorporate economic drivers of migration patterns and improving forecast accuracy.


## Durable Knowledge: TASK-0004 Completion
**Completed**: 2026-05-11 19:28:26
**Task**: TASK-0004-ingest-acled-data
**Expert Role**: Data Engineer
**Summary**: Successfully implemented automated extraction, transformation, and loading of ACLED conflict data for the refugee crisis prediction system.

**Key Implementation Details**:
- Verified ACLED connector's transform method works correctly with sample data
- Created ingestion script (ingest_acled.py) that uses existing IngestService framework
- Confirmed existing ACLED ingestion logic in IngestService is complete and handles multiple countries/date ranges
- Verified staging table for ACLED data exists (StagingConflict) with appropriate schema
- Implementation follows same proven pattern as UNHCR and World Bank data ingestion

**Files Created**:
- /ingest_acled.py (main execution script)

**Files Verified/Reviewed**:
- /backend/app/connectors/acled.py (ACLED connector)
- /backend/app/services/ingest_service.py (ingestion orchestration service)
- /backend/app/models/data_ingest.py (data models including StagingConflict)

**Next Steps Enabled**:
- Environment setup and end-to-end testing with database connection and API credentials
- Scheduled automated runs for regular conflict data updates
- Integration with conflict features in migration forecasting models
- Ability to filter by event types (battles, violence against civilians, etc.)

**Impact**: This implementation adds crucial conflict intensity data (battles, explosions, violence against civilians, protests, etc.) to the refugee crisis prediction system, enabling models to incorporate conflict drivers of migration patterns and improving forecast accuracy for conflict-induced displacement.
