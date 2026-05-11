# PROJECT_GOAL.md

## Project Name
Migration Forecasting System

## Current Product
The repository contains a comprehensive AI-powered platform for predicting forced migration patterns using multi-modal spatiotemporal data. It includes:
- Backend: FastAPI with PostgreSQL, Redis, Alembic migrations, ML model scaffolding, data connectors (UNHCR, World Bank, ACLED, NASA POWER)
- Frontend: React TypeScript placeholder (needs implementation)
- Documentation: Extensive docs covering data sources, architecture, implementation guide, deployment, UI design
- Docker-compose for local dev, render.yaml for Render deployment
- However, many components are incomplete or need refinement to reach world-class status.

## Goal For ROWS
Describe why ROWS is being added. Examples:
- Improve AI-assisted development discipline.
- Coordinate multiple workers safely.
- Require durable handoffs and verification evidence.
- Turn a large roadmap into claimable tasks.
Specifically for this project:
- Transform the existing codebase and documentation into a production-ready, world-class migration forecasting platform.
- Ensure all components (backend, frontend, ML, data pipelines, deployment) are fully implemented, tested, and documented.
- Establish a reliable, auditable development process using ROWS agent OS to manage tasks, handoffs, and verification.
- Achieve a system that can predict migration flows 4-26 weeks ahead with explainable AI, interactive visualizations, and robust deployment.

## In Scope
- Backend core infrastructure (already started)
- Data integration layer (connectors, ETL, validation)
- ML model implementation (LSTM, ensemble, training pipelines)
- Frontend development (interactive dashboard, maps, visualizations)
- Deployment and operations (Render, Docker, monitoring, scaling)
- Documentation updates to match implemented features
- Writing tests (unit, integration, end-to-end)
- Setting up CI/CD pipelines

## Out Of Scope
- Proprietary data sources requiring payment (focus on free APIs)
- Real-time streaming data processing (batch daily updates sufficient)
- Mobile applications (web-only focus)
- Multi-tenant SaaS features (single-instance deployment)
- Natural language query interface (beyond scope of MVP)

## Existing Constraints
- Runtime: Python 3.11+, Node.js 20+
- Package manager: pip, npm
- Framework: FastAPI (backend), React (frontend)
- Deployment target: Render (primary), Docker/Kubernetes (alternative)
- Security/compliance notes: Must handle data responsibly, no PII, follow provider rate limits and terms of service.

## First Milestone
The first milestone workers should decompose into task files is achieving a "Backend Core Complete" state where:
- All backend endpoints are implemented and tested
- Database schema is fully migrated and seeded with sample data
- Data ingestion pipelines run successfully for at least 3 data sources
- ML model training pipeline can execute end-to-end
- Basic API documentation is available via Swagger
- Docker-compose runs all services without errors
This milestone provides a stable foundation for frontend and advanced features.

## Human Owner Notes
Add any repo-specific judgment calls workers should preserve.
- Preserve the existing documentation structure; update rather than replace.
- Keep the MIT licensing and attribution to data providers.
- Maintain the separation of concerns between backend, frontend, and ML layers.
- Prefer using environment variables for configuration; do not hardcode secrets.
- When in doubt, follow the existing code style and patterns in the repository.