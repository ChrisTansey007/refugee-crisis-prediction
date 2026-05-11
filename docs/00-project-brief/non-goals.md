# Non-Goals

> **Customize after forking. Explicitly listing what is out of scope prevents scope creep.**

## Out of Scope

1. Proprietary data sources requiring payment — We focus on free, publicly available data sources to ensure accessibility and sustainability.
2. Real-time streaming data processing — Batch daily updates are sufficient for migration forecasting, which operates on weekly to monthly timescales.
3. Mobile applications — The initial focus is on a web-based dashboard; mobile apps may be considered in future phases.
4. Multi-tenant SaaS features — The system is designed for single-instance deployment per organization or use case.
5. Natural language query interface — While valuable, this is beyond the scope of the MVP and will be considered in later iterations.

## May Revisit Later

1. Mobile applications — When the web dashboard is stable and user feedback indicates a need for mobile access.
2. Real-time data ingestion — If specific use cases require sub-daily updates (e.g., flash flood or conflict escalation alerts).
3. Multi-tenancy — If multiple organizations seek to deploy isolated instances on shared infrastructure.
4. Advanced interaction features — Such as natural language querying or collaborative annotation.

## Related Files

- [`vision.md`](./vision.md) — Long-term vision
- [`current-scope.md`](./current-scope.md) — Current scope
- [`../01-product/roadmap.md`](../01-product/roadmap.md) — Product roadmap