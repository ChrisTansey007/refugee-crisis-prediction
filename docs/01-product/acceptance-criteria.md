# Acceptance Criteria

> **Customize after forking. Defines how we know a feature is done.**

## Format

Each criterion should be testable and unambiguous. Use the format: **Given [context], when [action], then [outcome].**

## Criteria by Feature

### Feature 1: Data Ingestion and Integration

- Given the system is running and configured with valid API keys, when the UNHCR ingestion job runs, then it should successfully fetch and store refugee data for the specified year and countries.
- Given new data is available from World Bank, when the ingestion job runs, then it should update the economic indicators table with the latest values.
- Given ACLED conflict data is available, when the ingestion job runs, then it should store conflict events with proper geographic coordinates and timestamps.
- Given NASA POWER climate data is available, when the ingestion job runs, then it should store climate parameters for the specified locations and date range.

### Feature 2: Migration Forecasting Models

- Given historical migration data and related indicators, when the LSTM model is trained, then it should produce forecasts with validation loss decreasing over epochs.
- Given trained models, when generating forecasts for a holdout period, then the mean absolute percentage error (MAPE) should be less than 25% for 8-week horizons.
- Given the ensemble model is configured, when making predictions, then it should combine outputs from individual models using weighted averaging.

### Feature 3: Explainable AI Dashboard

- Given the dashboard is loaded with forecast data, when a user selects a region and time period, then it should display the predicted migration flows on a map.
- Given a forecast has been generated, when the user requests explanation, then the system should show the top 3 contributing features with their impact scores.
- Given uncertainty quantification is enabled, when viewing a forecast, then the system should display confidence intervals around the point predictions.

### Feature 4: Data Validation and Quality Monitoring

- Given ingested data contains missing values, when validation runs, then it should flag records with missing required fields.
- Given ingested data contains values outside expected ranges, when validation runs, then it should flag these as potential outliers.
- Given a data source changes its format, when validation runs, then it should detect the schema mismatch and alert the engineering team.

### Feature 5: Scenario Analysis and What-If Modeling

- Given a baseline forecast exists, when the user modifies a driver variable (e.g., increases conflict intensity), then the system should generate a new forecast reflecting the change.
- Given two scenarios have been generated, when the user requests comparison, then the system should show the difference in predicted migration flows between them.

## Cross-Cutting Criteria

- Given a user interacts with the system, when an error occurs, then the system should display a user-friendly error message without exposing internal details.
- Given the system is under normal load, when a user requests a forecast, then the response should be returned within 5 seconds.
- Given the system is running, when health check endpoint is queried, then it should return a 200 status with service health information.
- Given data ingestion is scheduled, when the scheduled time arrives, then the ingestion process should start automatically without manual intervention.
- Given model training is scheduled, when the scheduled time arrives, then the training pipeline should start automatically.

## Related Files

- [`prd.md`](./prd.md) — Product requirements
- [`user-stories.md`](./user-stories.md) — User stories
- [`../../agent-os/definition-of-done.md`](../../agent-os/definition-of-done.md) — Definition of done