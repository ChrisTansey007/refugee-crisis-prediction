# Phase 5 Plan — Deployment, Ops & Advanced Features (Sprints 13–14)

Last Updated: 2025-10-13
Owner: DevOps Lead
Cross-Refs: DEPLOYMENT.md, ARCHITECTURE.md, IMPLEMENTATION_GUIDE.md, UI_DESIGN.md

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
- Harden production deployment (AWS ECS/K8s), security, monitoring, and alerting
- Optimize performance (DB indexes, caching, API tuning)
- Add advanced features (explainability hub UI, insights panel, scheduled reports)

## Non-Goals
- Major feature redesigns (fit-and-finish only)

---

## Sprint 13 (Week 25–26): Production Infra & Monitoring

### Objectives
- Set up production-ready infrastructure per `DEPLOYMENT.md`
- Enable monitoring, logging, and alerting with actionable runbooks

### Tasks
- Infrastructure
  - Provision AWS resources: ECS/Fargate (or EKS), RDS Postgres (Multi-AZ), ElastiCache Redis
  - Set up ALB with HTTPS via ACM; WAF rules; CloudFront for static assets
  - Configure Secrets Manager for JWT keys and DB credentials
- Observability
  - Prometheus scraping targets for API and worker
  - Grafana dashboards: API latency, ETL health, model accuracy
  - Alert rules: error rate >5%, DB pool >90%, ETL failures
- Security
  - JWT rotation policy; CSRF protection for forms; CORS whitelisting
  - Network security groups and least-privilege IAM roles
  - Image scanning and dependency scanning in CI

### Acceptance Criteria
- Blue/green or rolling deployment strategy works with zero downtime
- Dashboards populated and alerts firing under test conditions
- Secrets loaded at runtime; no secrets in repo

### Deliverables
- Terraform scripts (optional) + documentation
- Grafana JSONs; alert rules checked into repo
- Runbooks for common incidents (DB failover, cache flush, rate limits)

---

## Sprint 14 (Week 27–28): Performance & Advanced UX

### Objectives
- Optimize DB queries and API endpoints; reduce P95 latency
- Deliver “Explainability Hub”, “Insights Panel”, and scheduled report delivery

### Tasks
- Performance
  - Query tuning with `EXPLAIN ANALYZE`; add/adjust indexes
  - Redis caching for prediction and explainability endpoints
  - Batch APIs for multi-region requests
- Advanced UX
  - Explainability Hub modal (SHAP charts, factor trends, scenarios)
  - AI Insights Panel surfacing top anomalies and recommendations
  - Scheduled Reports delivery (email with PDF/HTML + CSV attachments)
- Reliability & Testing
  - Load testing (k6/Locust) to validate throughput/latency targets
  - E2E test suite for critical flows (map interactions, report export)

### Acceptance Criteria
- P95 latency < 500ms for key APIs; cache hit ratio > 60%
- Explainability Hub and Insights Panel function with real data
- Scheduled reports sent successfully with correct attachments

### Deliverables
- Performance report (before/after metrics)
- UX features implemented with docs and help overlays
- E2E test results captured in CI artifacts

---

## Exit Criteria (Phase Gate)
- Production deployment stable with monitoring and alerting
- Performance SLAs met for interactive features
- Operational runbooks validated and team trained
