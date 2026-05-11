# TASK-0004-ingest-acled-data

## Goal
Implement automated extraction, transformation, and loading of ACLED conflict data.

## Context
As a data engineer, I want to ingest ACLED conflict data so that I can measure conflict intensity as a driver of migration.

## Acceptance Criteria
- Successfully extract ACLED conflict data from the official API
- Transform data into the required schema for the migration database
- Load data into the appropriate tables with proper validation
- Achieve <5% data loss and <24 hour latency for daily updates
- Handle API rate limits and errors gracefully

## Steps
1. Review ACLED data API/documentation to understand available endpoints and data structure
2. Design database schema for storing ACLED conflict data (if not already defined)
3. Implement data extraction script with proper error handling and retry logic
4. Implement data transformation to match database schema
5. Implement data loading with transaction handling
6. Add validation checks to ensure data quality
7. Schedule automated runs (via cron or similar mechanism)
8. Monitor and log ingestion performance metrics

## Definition of Done
- ACLED data is successfully ingested and stored in the database
- Data meets quality thresholds (<5% loss, <24h latency)
- Ingestion process is automated and reliable
- Proper error handling and logging is in place