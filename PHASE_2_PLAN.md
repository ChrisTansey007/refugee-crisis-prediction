# Phase 2 Plan — Data Integration Layer (Sprints 4–6)

Last Updated: 2025-10-13
Owner: Data/Backend Lead
Cross-Refs: DATA_SOURCES.md, IMPLEMENTATION_GUIDE.md, ARCHITECTURE.md, DEPLOYMENT.md

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
- Build robust, rate-limit-aware connectors for priority sources (UNHCR, ACLED, NASA POWER, World Bank)
- Establish ETL orchestration with Celery schedules and retries
- Implement data validation (Great Expectations/Pandera) and provenance tracking
- Land data into Postgres/PostGIS with spatial indexing and partitioning

## Non-Goals
- No model training (Phase 3)
- No advanced streaming (optional in Phase 5)

---

## Sprint 4 (Week 7–8): UNHCR & World Bank Connectors

### Objectives
- Create UNHCR and World Bank ingestion with pagination and incremental updates
- Standardize schemas and write to staging tables

### Tasks
- UNHCR
  - Endpoint coverage: population, demographics
  - Params: year, country, limit/offset
  - Implement extractor with backoff + caching (Redis)
  - Normalize to `stg_unhcr_population` (document schema)
- World Bank
  - Endpoint coverage: indicators by country (GDP, CPI, unemployment)
  - Handle paging (`page`, `per_page`)
  - Normalize to `stg_worldbank_indicators`
- Common
  - Create `etl/clients/` and `etl/pipelines/` module structure
  - Add `extract() -> transform() -> load()` interfaces
  - Data validation: Pandera schema for each staging table

### Acceptance Criteria
- `celery beat` schedules UNHCR + World Bank nightly
- Staging tables populated; logs show counts and duration
- Validation failures logged and quarantined to `_errors` tables

### Deliverables
- ETL clients and pipelines for UNHCR + World Bank
- Staging schemas and validation definitions
- Docs updated in `DATA_SOURCES.md` (sample queries)

---

## Sprint 5 (Week 9–10): ACLED & NASA POWER Connectors

### Objectives
- Build ACLED and NASA POWER ingest with rate-limit handling and regional filtering
- Add geospatial join to admin regions (GADM) where applicable

### Tasks
- ACLED
  - Endpoint: `acled/read` with date windows (rolling 90 days)
  - Rate limiting guard + retries; delta sync strategy
  - Load to `stg_acled_events` with indexes on `event_date`, `country` and spatial (if lat/long)
- NASA POWER
  - Parameters: temporal average (daily), variables set (temp, precip, drought proxies)
  - Grid fetch strategy + caching
  - Load to `stg_power_climate`; map to regions using spatial aggregation (PostGIS)
- Common
  - Add Great Expectations suite for nulls, ranges, uniqueness
  - Provenance table: `data_ingest_runs` with source, params, counts, checksum

### Acceptance Criteria
- ACLED + NASA pipelines scheduled and runnable on demand
- Materialized view to aggregate climate to region/month created
- GE validation dashboard/report artifact saved to `data/validation/`

### Deliverables
- ACLED + NASA POWER pipelines
- PostGIS spatial functions and aggregation queries
- Data quality reports and provenance tracking

---

## Sprint 6 (Week 11–12): Consolidation, DQ, and Performance

### Objectives
- Consolidate staging into curated fact/dimension tables
- Add partitioning, indexes, and performance tuning
- Implement monitoring and alerting for ETL health

### Tasks
- Data Modeling
  - Dimensions: `dim_region`, `dim_date`, `dim_source`
  - Facts: `fact_displacement`, `fact_conflict`, `fact_climate`, `fact_economic`
  - Views: `vw_features_daily`, `vw_features_monthly`
- Performance
  - Partition large facts by month
  - Create indexes for joins and filters
  - VACUUM/ANALYZE cadence, `EXPLAIN ANALYZE` tuning
- Observability
  - Metrics: `etl_runs_total`, `etl_run_duration_seconds`, `etl_failures_total`
  - Alerts: pipeline failure, low row counts, late data

### Acceptance Criteria
- Curated tables populated and queries performant (< 1s typical filters)
- Monitoring dashboard shows ETL operational metrics
- Alert rules configured and tested

### Deliverables
- Curated data model and materialized views
- Partitioning and indexes documented
- ETL monitoring and alerting hooks

---

## Demo Script
- Show scheduled ETL runs and logs
- Query curated tables for last 30 days and display counts
- Demonstrate GE validation report artifact

---

## Exit Criteria (Phase Gate)
- 4 priority connectors running on schedule with validation and provenance
- Curated layer available for feature extraction (Phase 3)
- ETL performance and monitoring meet targets
