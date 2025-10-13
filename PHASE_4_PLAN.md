# Phase 4 Plan — Frontend Development (Sprints 10–12)

Last Updated: 2025-10-13
Owner: Frontend Lead
Cross-Refs: UI_DESIGN.md, ARCHITECTURE.md, DATA_SOURCES.md, IMPLEMENTATION_GUIDE.md

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
- Deliver an intuitive, accessible, and responsive UI aligned with `UI_DESIGN.md`
- Implement interactive maps, charts, and data source management UI
- Integrate with backend prediction and data APIs

## Non-Goals
- No advanced offline capabilities (consider in Phase 5)
- No multi-tenant features (beyond basic auth roles)

---

## Sprint 10 (Week 19–20): App Shell & Design System

### Objectives
- Create React + TypeScript app shell with routing, theming, and layout
- Implement core components and design tokens to match `UI_DESIGN.md`

### Tasks (Step-by-Step for Junior Dev)
- Bootstrapping
  - Initialize Vite React TS app
  - Add MUI 5, Emotion, React Router, Redux Toolkit
  - Set up ESLint + Prettier + TS strict mode
- App Shell
  - `AppLayout` with header, sidebar, content area
  - Route stubs: `/dashboard`, `/map`, `/analytics`, `/sources`, `/reports`
  - Global theme (colors, typography, spacing) per `UI_DESIGN.md`
- Reusable Components
  - `StatCard`, `KPIBar`, `SectionHeader`
  - Loading skeletons and empty states
- State & API Layer
  - Configure Redux Toolkit + RTK Query
  - Create base API slice with `/health` and `/stats` endpoints

### Acceptance Criteria
- App compiles with routes; theme matches design tokens
- Lint/test scripts pass; basic unit tests for components
- API layer successfully calls `/health` and shows status

### Deliverables
- Frontend scaffold with base components and routes
- Theme + tokens + reusable components

---

## Sprint 11 (Week 21–22): Interactive Map & Charts

### Objectives
- Implement the interactive map with layers, hover, and time slider
- Build key charts (time series, bar, heatmap) with interactivity

### Tasks
- Map
  - Integrate Mapbox GL JS (or Leaflet fallback)
  - Layers: heatmap, flows, points, predictions (toggle + opacity)
  - Hover tooltip + side panel; time slider
  - Presets for layer combinations
- Charts
  - Time series with brush/zoom and confidence intervals
  - Regional breakdown bar chart (click to filter)
  - Risk heatmap grid (click cell for details)
- Performance & Accessibility
  - Debounce hover, cluster markers, canvas rendering as needed
  - ARIA labels, keyboard navigation for key controls

### Acceptance Criteria
- Map supports hover and click interactions with smooth animation
- Charts support hover/zoom/brush, reflect filters across components
- Meets accessibility checklist from `UI_DESIGN.md`

### Deliverables
- Map and chart components integrated into `/dashboard` and `/map`

---

## Sprint 12 (Week 23–24): Data Sources & Report Builder

### Objectives
- Build Data Source Management with status, logs, and manual sync
- Implement Report Builder MVP with drag-and-drop widgets and export

### Tasks
- Data Sources UI
  - Card list with status indicators and quick actions
  - Filter/search/sort; modal for logs and configuration
  - Manual sync action with feedback
- Report Builder
  - Widget palette (map, time series, bar, heatmap, text, table)
  - Drag-and-drop canvas, resize, reorder
  - Export to PDF/HTML; schedule setup screen (stub API)
- Integration
  - Connect to backend endpoints for sources and reports
  - Add toasts/notifications for actions

### Acceptance Criteria
- Source cards show live status; logs accessible via modal
- Report canvas supports drag/drop and export to PDF/HTML
- Scheduled reports UI saves configuration (stubbed if backend not ready)

### Deliverables
- `/sources` and `/reports` pages
- User documentation updates for UI usage

---

## Demo Script
- Navigate app; show dashboard KPIs and live health
- Interact with map and charts; filter by region and time
- Open Data Sources; resync a source; show logs modal
- Build a report; drag widgets; export preview

---

## Exit Criteria (Phase Gate)
- Interactive map and charts meet performance and accessibility targets
- Data Sources UI functional with integration to backend
- Report Builder MVP usable for weekly briefs
