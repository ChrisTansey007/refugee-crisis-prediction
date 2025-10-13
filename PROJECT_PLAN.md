# Project Plan (Phased, Sprint-Based)

Last Updated: 2025-10-13
Owner: Product/Tech Leads

---

## Purpose
This plan breaks delivery into clear phases and 2-week sprints with actionable tasks, acceptance criteria, and links to detailed phase plans. It is designed so a junior developer can execute tasks step-by-step.

---

## Timeline Overview (Estimated 14 Sprints / ~28 Weeks)
- Phase 1: Backend Core Infrastructure — Sprints 1-3
- Phase 2: Data Integration Layer — Sprints 4-6
- Phase 3: ML Model Implementation — Sprints 7-9
- Phase 4: Frontend Development — Sprints 10-12
- Phase 5: Deployment, Ops & Hardening — Sprints 13-14

Note: Phases 2-4 can partially overlap once Phase 1 scaffolding and interfaces stabilize.

---

## Phase Plans (Detailed)
- Phase 1: Backend Core Infrastructure → [PHASE_1_PLAN.md](./PHASE_1_PLAN.md)
- Phase 2: Data Integration Layer → [PHASE_2_PLAN.md](./PHASE_2_PLAN.md)
- Phase 3: ML Model Implementation → [PHASE_3_PLAN.md](./PHASE_3_PLAN.md)
- Phase 4: Frontend Development → [PHASE_4_PLAN.md](./PHASE_4_PLAN.md)
- Phase 5: Deployment, Ops & Advanced → [PHASE_5_PLAN.md](./PHASE_5_PLAN.md)

---

## Roles & RACI
- Product Owner: Defines scope and accepts deliverables (A/R)
- Tech Lead: Architecture guardrails, reviews PRs (A/R)
- Backend Dev(s): API, ETL, DB, infra tasks (R)
- Frontend Dev(s): UI flows, charts, map, state (R)
- ML Engineer: Feature pipeline, models, serving (R)
- DevOps: CI/CD, infra, monitoring, security (R)
- Designer/UX: Wireframes, interaction patterns, accessibility (C)

---

## Engineering Ceremonies
- Sprint length: 2 weeks
- Planning: 2h per sprint (Day 1)
- Daily standup: 15 min
- Review + Demo: 1h (last day)
- Retrospective: 45 min (last day)
- Backlog grooming: 1h mid-sprint

---

## Branching & Workflow
- Default: `main` (protected), development: `develop`, feature branches: `feature/<ticket>`
- PRs require: lint, tests, 1+ reviewer approval, CI passing
- Conventional commits (e.g., `feat:`, `fix:`, `docs:`)

---

## Definition of Ready (DoR)
- Clear User Story with acceptance criteria
- Designs/wireframes referenced (`UI_DESIGN.md`)
- Dependencies identified (data, services, credentials)
- Test strategy known (unit/integration)

## Definition of Done (DoD)
- Code merged to `develop`, CI green
- Unit tests added (≥80% coverage for touched code)
- Docs updated (README sections, relevant .md files)
- Feature toggled/configurable; basic telemetry added

---

## Quality Gates
- Lint and formatting passing
- Unit tests passing
- Security checks (deps scan) passing
- Performance sanity checks for critical endpoints
- Manual QA checklist passed

---

## Risk & Mitigation (High-Level)
- API rate limits → caching, schedules, exponential backoff (see DATA_SOURCES.md)
- Data gaps/latency → quality checks, provenance, versioning
- Model drift → monitoring, retrain cadence, A/B evaluation
- Infra costs → scale to zero in non-peak, right-size instances, budgets

---

## Dependencies
- Data access to UNHCR, ACLED, NASA POWER, World Bank (free/public)
- Docker & container runtime
- Cloud accounts (if deploying to AWS/GCP/Azure)
- Mapbox token or Leaflet tiles (front-end)

---

## Communication
- Slack: #migration-forecasting (daily updates)
- Issue tracking: GitHub Projects/Issues
- Docs Single Source of Truth: this repository

---

## Cross-References
- Architecture → [ARCHITECTURE.md](./ARCHITECTURE.md)
- Data Sources → [DATA_SOURCES.md](./DATA_SOURCES.md)
- Implementation Guide → [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)
- Deployment → [DEPLOYMENT.md](./DEPLOYMENT.md)
- UI/UX → [UI_DESIGN.md](./UI_DESIGN.md)
- Readiness → [DEVELOPMENT_READINESS.md](./DEVELOPMENT_READINESS.md)

---

## Approval Gates per Phase
- Phase 1 Gate: API skeleton + DB + CI smoke tests + health checks
- Phase 2 Gate: 3 connectors live (UNHCR, ACLED, NASA) + DQ checks
- Phase 3 Gate: Baseline model served + accuracy dashboard + SHAP
- Phase 4 Gate: Interactive map + charts + data source UI + report builder MVP
- Phase 5 Gate: Production infra + monitoring + runbooks + launch checklist

---

## Estimation Guidance (for Junior Developers)
- Small task: ≤ 0.5 day (docs, config, minor UI)
- Medium task: 1–2 days (API endpoint, chart widget)
- Large task: 3–5 days (connector, complex map layer)
- Extra-large: Break down further before starting

---

## How to Use This Plan
1. Start with Phase 1 in sequence.
2. For each sprint, pick tasks in the Phase Plan with acceptance criteria.
3. Cross-check with `IMPLEMENTATION_GUIDE.md` for commands/examples.
4. Keep docs and PRs small and focused; ask for reviews early.
