# System Architecture

## Table of Contents
- [High-Level Architecture](#high-level-architecture)
- [Backend Structure](#backend-structure)
- [Frontend Structure](#frontend-structure)
- [Database Design](#database-design)
- [ML Pipeline](#ml-pipeline)
- [Technology Stack](#technology-stack)

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React)                         │
│  ┌──────────────┐  ┌───────────────┐  ┌─────────────────────┐  │
│  │  Dashboard   │  │  Map Viewer   │  │  Model Management   │  │
│  └──────────────┘  └───────────────┘  └─────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS/WebSocket
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API Gateway (FastAPI)                        │
└─────────────────────────────────────────────────────────────────┘
          │                    │                    │
          ▼                    ▼                    ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Data Pipeline   │  │  ML Services     │  │  Geo Services    │
└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
         └─────────────────────┼──────────────────────┘
                               ▼
         ┌─────────────────────────────────────────────┐
         │     PostgreSQL + PostGIS + Redis            │
         └─────────────────────────────────────────────┘
```

---

## Backend Structure

### Directory Layout
```
backend/
├── app/
│   ├── api/          # API endpoints
│   ├── core/         # Configuration & security
│   ├── models/       # Database models (SQLAlchemy)
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic
│   ├── ml/           # ML models & training
│   ├── workers/      # Celery background tasks
│   └── utils/        # Utilities
├── data/             # Local data storage
├── tests/            # Test suite
└── requirements.txt
```

### Key Services

**Migration Data Service**
```python
class MigrationDataService:
    async def ingest_unhcr_data(self) -> bool
    async def process_climate_indicators(self) -> bool
    async def update_conflict_metrics(self) -> bool
```

**Prediction Service**
```python
class PredictionService:
    async def train_model(self, config: ModelConfig) -> Model
    async def generate_forecast(self, region: str, horizon: int) -> Forecast
    async def explain_prediction(self, prediction_id: str) -> Explanation
```

**Geospatial Service**
```python
class GeoService:
    async def get_regional_boundaries(self) -> GeoJSON
    async def aggregate_to_grid(self, data: DataFrame, resolution: int) -> GridData
```

---

## Frontend Structure

### Directory Layout
```
frontend/
├── src/
│   ├── components/   # UI components
│   │   ├── Dashboard/
│   │   ├── MapVisualization/
│   │   ├── ModelManagement/
│   │   └── PredictionExplorer/
│   ├── pages/        # Page-level components
│   ├── services/     # API communication
│   ├── store/        # Redux state management
│   ├── hooks/        # Custom React hooks
│   ├── types/        # TypeScript definitions
│   └── utils/        # Utility functions
└── package.json
```

### Key Interfaces
```typescript
interface PredictionDashboard {
  models: ModelMetadata[];
  predictions: Forecast[];
  selectedRegion?: Region;
  timeRange: DateRange;
}

interface MapVisualization {
  layers: MapLayer[];
  predictions: SpatialPrediction[];
  onRegionSelect: (region: Region) => void;
}

interface Forecast {
  id: string;
  region: Region;
  predictions: PredictionPoint[];
  confidence: ConfidenceInterval;
  features: FeatureImportance[];
}
```

---

## Database Design

### Core Tables

**migration_events**
- Historical displacement data
- Origin/destination regions
- Population counts and types

**regions**
- Geographic boundaries (PostGIS)
- Population and area data
- Hierarchical structure

**indicators**
- Climate, economic, conflict metrics
- Time-series data
- Multi-source integration

**predictions**
- Model outputs
- Confidence intervals
- Feature importance

**models**
- Model registry
- Version control
- Performance metrics

**data_sources**
- API tracking
- Update schedules
- Data provenance

### Sample Schema
```sql
CREATE TABLE migration_events (
    id UUID PRIMARY KEY,
    event_date DATE NOT NULL,
    origin_region_id UUID REFERENCES regions(id),
    destination_region_id UUID REFERENCES regions(id),
    population_count INTEGER,
    event_type VARCHAR(50),
    data_source_id UUID REFERENCES data_sources(id)
);

CREATE TABLE regions (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    geometry GEOMETRY(MultiPolygon, 4326),
    population INTEGER,
    parent_region_id UUID REFERENCES regions(id)
);
```

---

## ML Pipeline

### Training Pipeline
```
Feature Store → Data Loader → Model Training → Validation → Model Registry → Deployment
```

### Model Architectures

**1. GeoTemporalLSTM**
```python
class GeoTemporalLSTM(nn.Module):
    # Geographic attention mechanism
    # Temporal sequence processing
    # Multi-head attention for feature fusion
```

**2. MultiModalPredictor**
```python
class MultiModalPredictor(nn.Module):
    self.cnn_branch     # Satellite imagery
    self.lstm_branch    # Time series
    self.fusion_layer   # Feature combination
```

**3. MigrationEnsemble**
```python
class MigrationEnsemble:
    self.models = [
        GeoTemporalLSTM(),
        XGBoostRegressor(),
        RandomForestRegressor()
    ]
```

### Inference Pipeline
```
Request → Feature Engineering → Model Inference → Post-processing → Explanation → Response
```

---

## Technology Stack

### Backend Core
- **Python**: 3.11+
- **API Framework**: FastAPI 0.104+
- **Database**: PostgreSQL 15+ with PostGIS 3.4+
- **Cache/Queue**: Redis 7.0+
- **Task Queue**: Celery 5.3+
- **ORM**: SQLAlchemy 2.0+
- **Validation**: Pydantic 2.0+

### Machine Learning
- **Deep Learning**: PyTorch 2.0+, PyTorch Lightning
- **Traditional ML**: scikit-learn 1.3+, XGBoost 2.0+, LightGBM 4.0+
- **Time Series**: Prophet, statsmodels, sktime
- **Geospatial**: GeoPandas, Shapely, Rasterio, PyProj
- **Interpretability**: SHAP 0.42+, LIME, Captum
- **Optimization**: Optuna 3.4+, Ray Tune

### Data Processing
- **DataFrames**: Pandas 2.0+, Polars
- **Parallel Processing**: Dask, Ray
- **Streaming**: Apache Kafka
- **Validation**: Great Expectations, Pandera
- **Formats**: PyArrow, Parquet, HDF5

### Frontend Core
- **Runtime**: Node.js 20+ LTS
- **Framework**: React 18+ with TypeScript 5.0+
- **Build Tool**: Vite 5.0+
- **Package Manager**: pnpm 8.0+

### UI/UX
- **Component Library**: Material-UI (MUI) 5.14+
- **Styling**: Emotion 11+
- **Icons**: Material Icons, Lucide React
- **Animations**: Framer Motion 10+

### State Management
- **State**: Redux Toolkit 2.0+ / Zustand
- **Server State**: TanStack Query v5
- **Forms**: React Hook Form 7.0+ with Zod
- **Routing**: React Router 6.16+

### Visualization
- **Charts**: Recharts 2.8+, D3.js 7.0+
- **Maps**: Mapbox GL JS 3.0+, React Map GL 7.0+
- **Geospatial**: Turf.js

### Infrastructure
- **Containerization**: Docker 24.0+
- **Orchestration**: Docker Compose, Kubernetes 1.28+
- **Cloud**: AWS/GCP/Azure
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack or Loki
- **Error Tracking**: Sentry

### Security
- **Authentication**: JWT with Auth0/Cognito
- **Encryption**: cryptography (Python), crypto-js (JS)
- **Secrets**: HashiCorp Vault, AWS Secrets Manager

### CI/CD
- **Pipeline**: GitHub Actions / GitLab CI
- **Testing**: Pytest, Vitest, Playwright
- **Code Quality**: ESLint, Prettier, Black, mypy
- **Coverage**: Coverage.py, c8

---

## Communication Patterns

### REST API
- Standard CRUD operations
- RESTful resource naming
- JSON request/response

### WebSockets
- Real-time prediction updates
- Training progress monitoring
- Alert notifications

### Message Queue
- Background data ingestion
- Batch prediction processing
- Model training orchestration

---

## Scaling Considerations

### Horizontal Scaling
- Multiple API server instances
- Load balancer distribution
- Stateless service design

### Database Optimization
- Read replicas for queries
- Spatial indexing (PostGIS)
- Connection pooling (PgBouncer)
- Partitioning for time-series data

### Caching Strategy
- Redis for API responses
- CDN for static assets
- Feature store for ML inputs

### Async Processing
- Celery workers for long tasks
- Kafka for event streaming
- Batch prediction scheduling

---

**Last Updated**: 2025-10-13
