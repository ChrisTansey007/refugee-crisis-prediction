# Current Scope

> **Customize after forking. Defines what is in scope for the current phase.**

## In Scope

1. Backend core infrastructure (FastAPI, PostgreSQL, Redis, data connectors)
2. Data integration layer (UNHCR, World Bank, ACLED, NASA POWER connectors)
3. ML model implementation (LSTM, ensemble models, training pipelines)
4. Frontend development (React TypeScript dashboard with maps and visualizations)
5. Deployment and operations (Docker-compose, Render deployment, monitoring)
6. Documentation updates to match implemented features
7. Writing tests (unit, integration, end-to-end)
8. Setting up CI/CD pipelines

## Phase

- **Current phase:** 1 - Foundation
- **Phase goal:** Establish a working backend core with data ingestion and basic ML model training

## Boundaries

- No mobile applications (web-only focus)
- No proprietary data sources requiring payment (focus on free APIs)
- No real-time streaming data processing (batch daily updates sufficient)
- No multi-tenant SaaS features (single-instance deployment)
- No natural language query interface (beyond scope of MVP)

## Related Files

- [`vision.md`](./vision.md) — Long-term vision
- [`non-goals.md`](./non-goals.md) — What is explicitly out
- [`../01-product/roadmap.md`](../01-product/roadmap.md) — Product roadmap