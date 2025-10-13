# UI/UX Design Specification

## Table of Contents
- [User Personas & Stories](#user-personas--stories)
- [User Journey Analysis](#user-journey-analysis)
- [UX Improvement Backlog](#ux-improvement-backlog)
- [Design System](#design-system)
- [Main Dashboard](#main-dashboard)
- [Interactive Map View](#interactive-map-view)
- [Analytics Dashboard](#analytics-dashboard)
- [Data Source Management](#data-source-management)
- [Report Builder](#report-builder)
- [Component Specifications](#component-specifications)

---

## User Personas & Stories

- **[Field Analyst – Crisis Alerting]**
  - **Level 1 (Epic)**: Spot new displacement hotspots and brief partners rapidly via the `UI_DESIGN.md` dashboard and map concepts.
  - **Level 2 (Stories)**: Access top five flagged regions with enriched hover tooltips; compare Somalia vs. Ethiopia; review AI insight panel for 24-hour anomalies.
  - **Level 3 (Acceptance)**: Time-to-first-insight ≤30s; tooltip response ≤200ms with displacement, risk, trend, drivers; exports mirror current map layers within ±5% variance.
- **[Data Engineer – Source Reliability]**
  - **Level 1 (Epic)**: Keep pipelines healthy using Data Source Management cards.
  - **Level 2 (Stories)**: Filter sources by status; trigger ACLED resync; act on alert-center notifications for rate limits or failures.
  - **Level 3 (Acceptance)**: Unhealthy sources highlighted <1 min; manual resync feedback ≤10s with log modal; alerts resolve automatically when status healthy.
- **[Humanitarian Planner – Forecast Brief]**
  - **Level 1 (Epic)**: Produce weekly briefs through Report Builder.
  - **Level 2 (Stories)**: Load Weekly Forecast template; drag “Top 3 Risks” widget; schedule Monday 08:00 UTC email delivery.
  - **Level 3 (Acceptance)**: Template load ≤5s; drag latency <100ms with live preview; scheduled delivery within 5 min with charts + data attachments.
- **[ML Scientist – Model Oversight]**
  - **Level 1 (Epic)**: Monitor accuracy, interpret SHAP insights, manage retraining via Analytics Dashboard.
  - **Level 2 (Stories)**: Review accuracy thresholds; launch SHAP explanations from region cards; schedule retraining with dataset selection.
  - **Level 3 (Acceptance)**: Accuracy alerts when <90%; SHAP modal loads ≤2s with feature importances and counterfactuals; retrain workflow logs model version metadata.
- **[Executive – High-Level Pulse]**
  - **Level 1 (Epic)**: Get mobile-friendly pulse of crises and data health.
  - **Level 2 (Stories)**: Open mobile summary; swipe through “Top Risks”; receive critical notifications.
  - **Level 3 (Acceptance)**: Mobile load <3s on 4G; swipe latency <150ms; alerts actionable directly from notification with response logging.

---

## User Journey Analysis

- **[Field Analyst Journey]**: Dashboard → global map → hotspot drill-down. Ensure layer legend stays unobtrusive, default time slider communicates current frame, and insight panel surfaces priority regions.
- **[Data Engineer Journey]**: Data Source view → status filters → log modal. Needs alert feed consolidation, batch actions, and contextual retry success messaging.
- **[Humanitarian Planner Journey]**: Report Builder → template load → drag widgets → schedule export. Provide wizard onboarding, inline data previews, and timezone confirmation.
- **[ML Scientist Journey]**: Analytics charts → SHAP modal → retrain dialog. Link explainability actions from map cards, add accuracy threshold alerts, and confirm dataset/version before retrain.
- **[Executive Journey]**: Mobile dashboard → quick actions → alert acknowledgments. Offer executive summary mode, bottom navigation, and tap-to-cycle hotspot cards.

---

## UX Improvement Backlog

- **[Guided Onboarding]**: Persona-specific walkthrough highlighting key controls (map layers, report templates, data health triage).
- **[Contextual Insights Panel]**: AI-generated anomaly summaries (rate limit warnings, rising risk regions) anchored to dashboard.
- **[Layer Presets & Defaults]**: Saved map layer combinations with user preferences for faster workflows.
- **[Centralized Alert Center]**: Filterable notification hub with acknowledgment workflow spanning data health, model drift, and risk spikes.
- **[Report Templates Library]**: Pre-built briefs (Weekly Forecast, Executive Summary, Model Review) with checklists for consistency.
- **[Explainability Hub]**: Dedicated modal aggregating SHAP plots, feature trends, and scenario comparisons accessible from map and analytics.
- **[Mobile Quick Actions]**: Compact top-level buttons for Top Risks, Latest Alerts, Data Health plus swipeable cards for hotspot exploration.
- **[Accessibility Enhancements]**: Colorblind-safe palettes, keyboard shortcuts for layer toggles, data table exports for charts to reinforce WCAG goals.

---

## Design System

### Color Palette

**Primary Colors**
```css
--primary: #2563eb        /* Blue - Main actions */
--primary-hover: #1e40af  /* Darker blue - Hover states */
--secondary: #8b5cf6      /* Purple - Secondary actions */
--accent: #06b6d4         /* Cyan - Highlights */
```

**Semantic Colors**
```css
--success: #10b981        /* Green */
--warning: #f59e0b        /* Orange */
--danger: #ef4444         /* Red */
--info: #06b6d4           /* Cyan */
```

**Risk Level Colors**
```css
--risk-low: #10b981       /* Green */
--risk-medium: #f59e0b    /* Yellow/Orange */
--risk-high: #f97316      /* Orange */
--risk-critical: #dc2626  /* Dark Red */
```

**Data Visualization Palette**
```css
--viz-1: #3b82f6   /* Blue */
--viz-2: #22c55e   /* Green */
--viz-3: #a855f7   /* Purple */
--viz-4: #fb923c   /* Orange */
--viz-5: #ec4899   /* Pink */
--viz-6: #14b8a6   /* Teal */
```

### Typography

```css
Font: 'Inter' (Primary), 'Roboto Mono' (Code)

Sizes:
- Heading 1: 36px / 600 weight
- Heading 2: 30px / 600 weight
- Heading 3: 24px / 600 weight
- Body Large: 18px / 400 weight
- Body: 16px / 400 weight
- Body Small: 14px / 400 weight
- Caption: 12px / 400 weight
```

### Spacing System (8px Grid)

```
4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px, 96px
```

---

## Main Dashboard

### Layout Structure

```
+----------------------------------------------------------------+
|  [Logo] Migration Forecasting System    🔔 Alerts  👤 Profile  |
+----------------------------------------------------------------+
|  📊 Dashboard  |  🗺️ Map  |  📈 Analytics  |  ⚙️ Data Sources  |
+----------------------------------------------------------------+
|                                                                |
|  +---------------+  +---------------+  +---------------+       |
|  | 🌍 Total      |  | 🎯 High Risk  |  | 📈 Trend      |       |
|  | Displaced     |  | Countries     |  | This Week     |       |
|  |               |  |               |  |               |       |
|  | 2.5M          |  |   47          |  |  ↑ 12%        |       |
|  | +12% vs last  |  |   +5 new      |  |  567K new     |       |
|  +---------------+  +---------------+  +---------------+       |
|                                                                |
|  +--------------------------------------------------------+   |
|  |  🌍 GLOBAL MIGRATION MAP                    [🔍 Search] |   |
|  |                                                          |   |
|  |         [Hover Tooltip]                                  |   |
|  |    ┌─────────────────────┐                              |   |
|  |    │ 📍 Somalia          │                              |   |
|  | ●  │ Displaced: 2.1M     │    ● ● ●                     |   |
|  |  ● │ Risk: 🔴 High       │   ●●●●●                      |   |
|  | ●●●│ 30-day trend: ↑15%  │  ●●  ●●                      |   |
|  |  ● │ [View Details →]    │   ● ●                        |   |
|  |    └─────────────────────┘                              |   |
|  |                                                          |   |
|  |  Controls: [Heat] [Flow] [Points] Time: ◀ ●═══════ ▶   |   |
|  +--------------------------------------------------------+   |
|                                                                |
|  +---------------------------+  +--------------------------+   |
|  | 📊 MIGRATION TRENDS       |  | 🎯 MODEL PERFORMANCE     |   |
|  |                           |  |                          |   |
|  | [Interactive Line Chart]  |  | [Performance Metrics]    |   |
|  |                           |  |                          |   |
|  | ▲ 3M                      |  | • LSTM:     94.2% ━━━━○  |   |
|  | │    ╱─╲    ╱─╲           |  | • XGBoost:  91.8% ━━━○   |   |
|  | │   ╱   ╲  ╱   ╲          |  | • Ensemble: 95.1% ━━━━●  |   |
|  | │  ╱     ╲╱     ╲         |  |                          |   |
|  | ┼────────────────────▶    |  | [Retrain Models]         |   |
|  |   Q1   Q2   Q3   Q4       |  |                          |   |
|  +---------------------------+  +--------------------------+   |
|                                                                |
+----------------------------------------------------------------+
```

### Key Features

**1. Stat Cards (Top Row)**
- Real-time metrics with sparklines
- Color-coded trend indicators
- Click to drill down
- Animated number counters

**2. Interactive Map**
- Multi-layer support (heatmap, flow, points)
- Hover tooltips with rich information
- Click regions for detailed view
- Time slider for historical playback
- Smooth zoom/pan animations

**3. Quick Insights**
- Live updating charts
- Comparative analysis
- Exportable reports

---

## Interactive Map View

### Full Screen Map Interface

```
+----------------------------------------------------------------+
| [← Back] 🗺️ Interactive Map View              [⚙️] [📤 Share] |
+----------------------------------------------------------------+
|                                                                |
| +----------+  Map Controls:                                    |
| | LAYERS   |  ☑️ Migration Flows    ☐ Population Density      |
| |----------|  ☑️ Conflict Events    ☐ Climate Zones           |
| | □ Flows  |  ☑️ Risk Heatmap       ☐ Economic Indicators     |
| | ☑️ Heat   |  ☑️ Predictions        ☐ Border Crossings        |
| | ☑️ Points |                                                  |
| | □ 3D     |  Time Range: [Jan 2024] ━━━●━━━━━━━ [Dec 2024]  |
| +----------+                                                   |
|                                                                |
|  +--------------------------------------------------------+   |
|  |                                                        |   |
|  |                  🌍 MAP CANVAS                        |   |
|  |                                                        |   |
|  |     [Hover Card Appears on Region Hover]              |   |
|  |  ┌────────────────────────────────────┐               |   |
|  |  │ 📍 South Sudan                     │               |   |
|  |  │ ─────────────────────────────────  │               |   |
|  |  │                                    │  ●            |   |
|  |  │ 👥 Current Displaced: 2.1M         │ ● ●═══╗      |   |
|  |  │ 📊 Predicted (30d):   2.4M         │  ●●   ║      |   |
|  |  │ 📈 Change:           +14% ↑        │   ●   ║      |   |
|  |  │                                    │       ║      |   |
|  |  │ Risk Assessment:                   │       ▼      |   |
|  |  │ ████████████████░░░░ 🔴 High       │      ●●      |   |
|  |  │                                    │     ● ●      |   |
|  |  │ Contributing Factors:              │               |   |
|  |  │ • 🌡️ Drought severity: High        │               |   |
|  |  │ • ⚔️ Conflict intensity: Medium     │               |   |
|  |  │ • 💰 Economic stress: High          │               |   |
|  |  │                                    │               |   |
|  |  │ Last updated: 2 hours ago          │               |   |
|  |  │                                    │               |   |
|  |  │ [View Full Report] [Track]         │               |   |
|  |  └────────────────────────────────────┘               |   |
|  |                                                        |   |
|  |  🔍 [Search Location...]           [📍] [🎯] [📥]     |   |
|  +--------------------------------------------------------+   |
|                                                                |
| Legend:                                                        |
| 🟢 Low  🟡 Medium  🟠 High  🔴 Critical  ━━→ Flow  ● Event    |
|                                                                |
+----------------------------------------------------------------+
```

### Map Interactions

**Hover Effects:**
- Smooth highlight on region hover
- Rich tooltip with key metrics
- Preview of trends
- Quick action buttons

**Click Actions:**
- Drill down to detailed view
- Open side panel with full data
- Compare with other regions
- Export region data

**Layer Controls:**
- Toggle multiple layers
- Adjust opacity
- Filter by data type
- Custom layer combinations

**Time Controls:**
- Play/pause animation
- Scrub through timeline
- Preset time ranges
- Speed control

---

## Analytics Dashboard

```
+----------------------------------------------------------------+
| 📈 Analytics & Insights                    [📅 Last 30 Days ▼] |
+----------------------------------------------------------------+
|                                                                |
| +--------------------------------------------------------+   |
| | TIME SERIES ANALYSIS                     [Export 📥]   |   |
| |                                                        |   |
| |  3.0M │                    ╱──╲              [Toggle: |   |
| |       │                ╱──╱    ╲                      |   |
| |  2.5M │            ╱──╱          ╲──╲         □ Actual|   |
| |       │        ╱──╱                  ╲        ☑️ Pred. |   |
| |  2.0M │    ╱──╱                       ╲──╲    □ Conf. |   |
| |       │╱──╱                               ╲          |   |
| |  1.5M ┼─────────────────────────────────────────▶    |   |
| |       Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep    |   |
| |                                                        |   |
| | [Hover shows]: Apr 15: 2.3M (↑5.2%) Pred: 2.35M      |   |
| +--------------------------------------------------------+   |
|                                                                |
| +---------------------------+  +--------------------------+   |
| | 🌍 REGIONAL BREAKDOWN     |  | 📊 CONTRIBUTING FACTORS  |   |
| |                           |  |                          |   |
| | [Interactive Bar Chart]   |  | [Stacked Area Chart]     |   |
| |                           |  |                          |   |
| | Africa    ████████░ 45%   |  |     ┌─Climate            |   |
| | M.East    ██████░░░ 30%   |  |     │╱╲╱╲╱╲              |   |
| | Asia      ████░░░░░ 20%   |  |     │    ╱╲╱╲╱─Conflict  |   |
| | Americas  ██░░░░░░░  5%   |  |     │  ╱Economic         |   |
| |                           |  |     │╱                   |   |
| | [Click region to filter]  |  |     └──────────────▶     |   |
| +---------------------------+  +--------------------------+   |
|                                                                |
| +---------------------------+  +--------------------------+   |
| | 🎯 PREDICTION ACCURACY    |  | 🔥 RISK HEATMAP          |   |
| |                           |  |                          |   |
| | Model Comparison:         |  | [Grid Heatmap]           |   |
| |                           |  |                          |   |
| | LSTM                      |  | Risk by Region & Factor: |   |
| | ████████████████ 94.2%    |  |           Clim Conf Econ |   |
| |                           |  | Somalia   🔴   🟠   🔴   |   |
| | XGBoost                   |  | Yemen     🔴   🔴   🟠   |   |
| | ██████████████░░ 91.8%    |  | Sudan     🟠   🔴   🟠   |   |
| |                           |  | Afghanis  🟡   🔴   🟠   |   |
| | Ensemble                  |  |                          |   |
| | █████████████████ 95.1%   |  | [Click cell for details] |   |
| |                           |  |                          |   |
| | [View Detailed Report →]  |  | [Download CSV]           |   |
| +---------------------------+  +--------------------------+   |
|                                                                |
+----------------------------------------------------------------+
```

### Interactive Chart Features

**1. Time Series Chart**
- Hover: Show exact values, predictions, confidence intervals
- Click: Zoom into time period
- Drag: Select date range
- Toggle: Show/hide data series
- Animate: Play through time

**2. Regional Breakdown**
- Hover: Highlight region
- Click: Filter all charts by region
- Drag bars: Reorder by custom metric
- Export: Download data

**3. Factor Analysis**
- Stacked area for multiple factors
- Toggle factor visibility
- Smooth transitions
- Color-coded by importance

**4. Risk Heatmap**
- Color gradient for risk levels
- Click cells for detailed breakdown
- Hover for quick stats
- Export as image/data

---

## Data Source Management

```
+----------------------------------------------------------------+
| ⚙️ Data Source Management                   [+ Add New Source] |
+----------------------------------------------------------------+
|                                                                |
| [🔍 Search sources...]  [Filter: All ▼] [Sort: Status ▼]      |
|                                                                |
| +--------------------------------------------------------+   |
| | DATA SOURCES                            [Refresh All 🔄] |   |
| |                                                          |   |
| | +------------------------------------------------------+ |   |
| | | 📊 UNHCR Refugee Statistics API        ✅ Active     | |   |
| | |─────────────────────────────────────────────────────| |   |
| | | Base URL: https://api.unhcr.org/population/v1/      | |   |
| | | Update Frequency: Daily at 02:00 UTC               | |   |
| | | Last Sync: 2 hours ago ✓                           | |   |
| | |                                                     | |   |
| | | Status:  ●●●●●●●●●○ 90% Healthy                   | |   |
| | |                                                     | |   |
| | | Recent Stats:                                       | |   |
| | | • Records fetched: 1,247,893                       | |   |
| | | • Success rate: 99.8%                              | |   |
| | | • Avg response: 245ms                              | |   |
| | |                                                     | |   |
| | | [📊 View Logs] [⚙️ Configure] [🔄 Sync Now]        | |   |
| | +------------------------------------------------------+ |   |
| |                                                          |   |
| | +------------------------------------------------------+ |   |
| | | ⚔️ ACLED Conflict Events              ⚠️ Warning     | |   |
| | |─────────────────────────────────────────────────────| |   |
| | | Base URL: https://api.acleddata.com/acled/read     | |   |
| | | Update Frequency: Every 6 hours                    | |   |
| | | Last Sync: 14 min ago ✓                           | |   |
| | |                                                     | |   |
| | | Status:  ●●●●●●●●○○ 80% (Rate limit approaching)  | |   |
| | |                                                     | |   |
| | | ⚠️ Alert: Approaching daily rate limit             | |   |
| | | API Calls: 8,970 / 10,000 remaining                | |   |
| | |                                                     | |   |
| | | [📊 View Logs] [⚙️ Configure] [🔄 Sync Now]        | |   |
| | +------------------------------------------------------+ |   |
| |                                                          |   |
| | +------------------------------------------------------+ |   |
| | | 🌡️ NASA POWER Climate Data            ✅ Active     | |   |
| | |─────────────────────────────────────────────────────| |   |
| | | Base URL: https://power.larc.nasa.gov/api/         | |   |
| | | Update Frequency: Daily                            | |   |
| | | Last Sync: 6 hours ago ✓                          | |   |
| | |                                                     | |   |
| | | Status:  ●●●●●●●●●● 100% Healthy                  | |   |
| | |                                                     | |   |
| | | Coverage: 245 regions, 12 parameters               | |   |
| | | Data points: 3.2M                                  | |   |
| | |                                                     | |   |
| | | [📊 View Logs] [⚙️ Configure] [🔄 Sync Now]        | |   |
| | +------------------------------------------------------+ |   |
| |                                                          |   |
| | +------------------------------------------------------+ |   |
| | | 💰 World Bank Indicators           ✅ Active       | |   |
| | | 👥 WorldPop Population Data        ✅ Active       | |   |
| | | 🌍 GDELT Global Events             🔄 Syncing...   | |   |
| | | 🗺️ GADM Administrative Boundaries   ✅ Active       | |   |
| | +------------------------------------------------------+ |   |
| |                                                          |   |
| +--------------------------------------------------------+   |
|                                                                |
| +--------------------------------------------------------+   |
| | SYNC SCHEDULE                                          |   |
| |                                                        |   |
| | Next scheduled syncs:                                  |   |
| | • UNHCR:      Tomorrow at 02:00 UTC                   |   |
| | • ACLED:      In 4 hours                              |   |
| | • NASA POWER: Tomorrow at 00:00 UTC                   |   |
| |                                                        |   |
| | [Edit Schedule] [Manual Sync All]                     |   |
| +--------------------------------------------------------+   |
|                                                                |
+----------------------------------------------------------------+
```

### Data Source Card Features

**Status Indicators:**
- ✅ Active (Green)
- ⚠️ Warning (Yellow)
- ❌ Error (Red)
- 🔄 Syncing (Blue animated)
- ⏸️ Paused (Gray)

**Health Metrics:**
- Visual progress bar
- Success rate percentage
- Response time
- Error count

**Quick Actions:**
- View detailed logs
- Configure settings
- Manual sync trigger
- Pause/resume sync

**Expandable Details:**
- Click card to expand
- Show full configuration
- Historical sync data
- Error logs

---

## Report Builder

```
+----------------------------------------------------------------+
| 📄 Report Builder                               [Save] [Export]|
+----------------------------------------------------------------+
|                                                                |
| Report Name: [Q3 2024 Migration Analysis_________________]     |
| Template:    [Custom Report ▼] [Load Template]                |
|                                                                |
| +---------------------------+  +--------------------------+   |
| | 📊 AVAILABLE WIDGETS      |  | 📋 REPORT CANVAS         |   |
| |                           |  |                          |   |
| | Drag to canvas:           |  | ┌──────────────────────┐ |   |
| |                           |  | │ 📊 Executive Summary │ |   |
| | 📈 Time Series Chart      |  | └──────────────────────┘ |   |
| | 🗺️ Map Visualization      |  |                          |   |
| | 📊 Bar Chart              |  | ┌──────────────────────┐ |   |
| | 🔥 Heatmap                |  | │ 🗺️ [Drop Zone]       │ |   |
| | 📉 Line Chart             |  | │                      │ |   |
| | 🥧 Pie Chart              |  | │ Drag widget here or  │ |   |
| | 📋 Data Table             |  | │ [+ Add Widget]       │ |   |
| | 📝 Text Block             |  | └──────────────────────┘ |   |
| | 🎯 Metric Card            |  |                          |   |
| | 📊 Comparison Chart       |  | ┌──────────────────────┐ |   |
| |                           |  | │ 📈 Migration Trends  │ |   |
| | Filters:                  |  | │                      │ |   |
| | • Date Range              |  | │ [Chart Preview]      │ |   |
| | • Regions                 |  | │                      │ |   |
| | • Data Sources            |  | │ [⚙️ Configure]       │ |   |
| | • Risk Levels             |  | └──────────────────────┘ |   |
| |                           |  |                          |   |
| +---------------------------+  | [+ Add Section]          |   |
|                                |                          |   |
| +------------------------------------------------------+  |   |
| | EXPORT OPTIONS                                       |  |   |
| |                                                      |  |   |
| | Format:  ○ PDF  ○ Excel  ○ PowerPoint  ○ HTML       |  |   |
| | Include: ☑️ Raw Data  ☑️ Charts  ☑️ Executive Summary |  |   |
| | Quality: [High ▼]  Schedule: [One-time ▼]           |  |   |
| |                                                      |  |   |
| | [Generate Report] [Schedule Delivery]                |  |   |
| +------------------------------------------------------+  |   |
|                                +--------------------------+   |
|                                                                |
+----------------------------------------------------------------+
```

### Report Features

**Drag & Drop Interface:**
- Intuitive widget placement
- Resize widgets
- Reorder sections
- Delete with animation

**Widget Configuration:**
- Click widget to configure
- Set data sources
- Apply filters
- Customize appearance

**Real-time Preview:**
- See changes instantly
- Interactive charts in builder
- Responsive layout preview

**Export Options:**
- PDF with vector graphics
- Excel with data tables
- PowerPoint slides
- Interactive HTML

**Scheduled Reports:**
- Daily, weekly, monthly
- Email delivery
- Auto-generate and send
- Version control

---

## Component Specifications

### 1. Interactive Map Component

**Technology:** Mapbox GL JS + React Map GL

```typescript
interface MapComponentProps {
  layers: MapLayer[];
  center: [number, number];
  zoom: number;
  onRegionHover: (region: Region) => void;
  onRegionClick: (region: Region) => void;
  timeRange: DateRange;
  filters: MapFilters;
}

interface MapLayer {
  id: string;
  type: 'heatmap' | 'flow' | 'point' | 'polygon';
  data: GeoJSON;
  visible: boolean;
  opacity: number;
  style: LayerStyle;
}
```

**Features:**
- Smooth zoom transitions (800ms ease-out)
- Hover effects with 150ms delay
- Clustering for > 100 points
- WebGL-powered rendering
- Responsive to container size

### 2. Time Series Chart Component

**Technology:** Recharts / D3.js

```typescript
interface TimeSeriesChartProps {
  data: TimeSeriesData[];
  predictions?: PredictionData[];
  confidenceInterval?: ConfidenceData[];
  onHover: (point: DataPoint) => void;
  onBrush: (range: DateRange) => void;
  interactive: boolean;
}
```

**Interactions:**
- Hover: Show tooltip with details
- Click: Pin tooltip
- Drag: Select time range
- Zoom: Scroll to zoom in/out
- Pan: Drag to move view

### 3. Data Source Card Component

```typescript
interface DataSourceCardProps {
  source: DataSource;
  expanded: boolean;
  onSync: () => Promise<void>;
  onConfigure: () => void;
  onViewLogs: () => void;
}

interface DataSource {
  id: string;
  name: string;
  status: 'active' | 'warning' | 'error' | 'syncing';
  health: number; // 0-100
  lastSync: Date;
  nextSync: Date;
  metrics: SourceMetrics;
}
```

**Animations:**
- Expand/collapse: 300ms ease-in-out
- Status pulse: 2s infinite for syncing
- Health bar: Smooth fill animation

### 4. Hover Tooltip Component

```typescript
interface TooltipProps {
  position: { x: number; y: number };
  data: TooltipData;
  interactive?: boolean;
  delay?: number; // default 200ms
}
```

**Behavior:**
- Appear after delay
- Follow cursor smoothly
- Stay within viewport
- Dismiss on click outside
- Support rich content (charts, lists)

---

## Responsive Design

### Breakpoints

```css
/* Mobile */
@media (max-width: 640px) {
  /* Stack cards vertically */
  /* Simplified map controls */
  /* Bottom sheet for details */
}

/* Tablet */
@media (min-width: 641px) and (max-width: 1024px) {
  /* 2-column grid */
  /* Side panel for map details */
}

/* Desktop */
@media (min-width: 1025px) {
  /* Full 3-column grid */
  /* Floating panels */
  /* Advanced controls */
}
```

### Mobile Optimizations

- Touch-friendly controls (min 44px)
- Swipe gestures for navigation
- Bottom sheet for details
- Simplified visualizations
- Lazy loading images
- Progressive enhancement

---

## Performance Optimizations

### Chart Performance

- Virtual scrolling for large datasets (>1000 points)
- Canvas rendering for complex visualizations
- Debounce hover events (150ms)
- Lazy load off-screen charts
- Memoize expensive calculations

### Map Performance

- Cluster markers (>100 points)
- Simplify geometries at low zoom
- Tile-based rendering
- Progressive loading
- WebGL acceleration

### Data Loading

- Skeleton screens while loading
- Pagination for tables (50 rows)
- Infinite scroll for lists
- Cache API responses (5 min)
- Optimistic UI updates

---

## Accessibility (WCAG 2.1 AA)

### Color Contrast

- Text: Minimum 4.5:1 ratio
- UI elements: Minimum 3:1 ratio
- Risk colors: Patterns for colorblind users

### Keyboard Navigation

- Tab through all interactive elements
- Arrow keys for chart navigation
- Enter/Space to activate
- Escape to close modals
- Focus indicators (3px outline)

### Screen Readers

- ARIA labels for all controls
- Chart data tables for screen readers
- Live regions for updates
- Descriptive alt text
- Semantic HTML structure

---

## Animation Specifications

### Transition Timing

```css
/* Quick actions */
--duration-fast: 150ms;

/* Standard transitions */
--duration-normal: 300ms;

/* Complex animations */
--duration-slow: 500ms;

/* Data visualizations */
--duration-viz: 800ms;

/* Easing */
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
```

### Chart Animations

- Line charts: Draw path animation (800ms)
- Bar charts: Height animation (600ms)
- Pie charts: Rotation + arc animation (700ms)
- Map layers: Fade in (400ms)
- Numbers: Count up animation (1000ms)

### Micro-interactions

- Button press: Scale 0.95 (100ms)
- Card hover: Lift shadow (200ms)
- Toggle switch: Slide (250ms)
- Dropdown: Slide down (200ms)
- Toast notifications: Slide in from right (300ms)

---

**Last Updated:** 2025-10-13  
**Design Version:** 1.0  
**Figma File:** [Link to design mockups]
