# Implementation Guide

## Table of Contents
- [Phase 1: Backend Core Infrastructure](#phase-1-backend-core-infrastructure)
- [Phase 2: Data Integration Layer](#phase-2-data-integration-layer)
- [Phase 3: ML Model Implementation](#phase-3-ml-model-implementation)
- [Phase 4: Frontend Development](#phase-4-frontend-development)
- [Phase 5: Advanced Features](#phase-5-advanced-features)
- [Development Workflow](#development-workflow)
- [Testing Strategy](#testing-strategy)

---

## Phase 1: Backend Core Infrastructure

**Duration**: 2-3 weeks  
**Goal**: Set up foundational backend architecture and database

### 1.1 Project Setup & Environment

#### Step 1: Initialize Project Structure
```bash
mkdir -p backend/{app/{api/v1,core,models,schemas,services,ml,workers,utils},data,tests}
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

#### Step 2: Create requirements.txt
```txt
# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.23
asyncpg==0.29.0
alembic==1.13.0
psycopg2-binary==2.9.9
geoalchemy2==0.14.2

# Cache & Queue
redis==5.0.1
celery==5.3.4

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Data Processing
pandas==2.1.4
numpy==1.26.2
geopandas==0.14.1
shapely==2.0.2

# Utilities
httpx==0.25.2
python-dotenv==1.0.0
```

#### Step 3: Create .env.example
```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/migration_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Settings
API_V1_PREFIX=/api/v1
PROJECT_NAME=Migration Forecasting System
```

#### Step 4: Set up FastAPI Application
```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, migrations, predictions

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["auth"])
app.include_router(migrations.router, prefix=f"{settings.API_V1_PREFIX}/migrations", tags=["migrations"])
app.include_router(predictions.router, prefix=f"{settings.API_V1_PREFIX}/predictions", tags=["predictions"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### 1.2 Database Schema Implementation

#### Step 1: Configure SQLAlchemy
```python
# app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session
```

#### Step 2: Create Base Models
```python
# app/models/base.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
from datetime import datetime

Base = declarative_base()

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

#### Step 3: Implement Core Models
```python
# app/models/region.py
from sqlalchemy import Column, String, Integer, Float, UUID, ForeignKey
from geoalchemy2 import Geometry
from app.models.base import Base, TimestampMixin
import uuid

class Region(Base, TimestampMixin):
    __tablename__ = "regions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    iso_code = Column(String(10))
    region_type = Column(String(50))
    geometry = Column(Geometry('MULTIPOLYGON', srid=4326))
    population = Column(Integer)
    area_km2 = Column(Float)
    parent_region_id = Column(UUID(as_uuid=True), ForeignKey('regions.id'))
```

#### Step 4: Set up Alembic
```bash
alembic init alembic
```

Edit `alembic/env.py` to include your models and configure async support.

### 1.3 Core API Endpoints

#### Authentication Endpoints
```python
# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, Token
from app.services.user_service import UserService

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user: UserCreate, service: UserService = Depends()):
    return await service.create_user(user)

@router.post("/login", response_model=Token)
async def login(email: str, password: str, service: UserService = Depends()):
    return await service.authenticate(email, password)
```

#### Data Endpoints
```python
# app/api/v1/migrations.py
from fastapi import APIRouter, Depends, Query
from typing import List
from app.schemas.migration import MigrationEvent
from app.services.migration_service import MigrationDataService

router = APIRouter()

@router.get("/events", response_model=List[MigrationEvent])
async def get_migration_events(
    region_id: str,
    start_date: str,
    end_date: str,
    service: MigrationDataService = Depends()
):
    return await service.get_events(region_id, start_date, end_date)

@router.post("/ingest/unhcr")
async def trigger_unhcr_ingestion(
    year: int,
    service: MigrationDataService = Depends()
):
    return await service.ingest_unhcr_data(year)
```

---

## Phase 2: Data Integration Layer

**Duration**: 3-4 weeks  
**Goal**: Implement data connectors and ETL pipelines

### 2.1 Data Source Connectors

#### UNHCR Data Connector
```python
# app/services/connectors/unhcr_connector.py
import httpx
from typing import List, Dict
from app.core.logging import logger

class UNHCRConnector:
    BASE_URL = "https://api.unhcr.org/population/v1"
    
    async def fetch_population_data(self, year: int) -> List[Dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/population/",
                params={"year": year, "limit": 10000}
            )
            response.raise_for_status()
            return response.json()
    
    async def fetch_demographics(self, country_code: str, year: int) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/demographics/",
                params={"coo_iso": country_code, "year": year}
            )
            response.raise_for_status()
            return response.json()
```

#### ACLED Conflict Data Connector
```python
# app/services/connectors/acled_connector.py
import httpx
from app.core.config import settings

class ACLEDConnector:
    BASE_URL = "https://api.acleddata.com/acled/read"
    
    def __init__(self):
        self.api_key = settings.ACLED_API_KEY
        self.email = settings.ACLED_EMAIL
    
    async def fetch_events(self, country: str, start_date: str, end_date: str):
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                self.BASE_URL,
                params={
                    "key": self.api_key,
                    "email": self.email,
                    "country": country,
                    "event_date": f"{start_date}|{end_date}",
                    "event_date_where": "BETWEEN"
                }
            )
            response.raise_for_status()
            return response.json()
```

#### Climate Data Connector (NASA POWER)
```python
# app/services/connectors/climate_connector.py
import httpx
from typing import Dict

class NASAPowerConnector:
    BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
    
    async def fetch_climate_data(
        self, 
        latitude: float, 
        longitude: float,
        start_date: str,
        end_date: str,
        parameters: str = "T2M,PRECTOTCORR"
    ) -> Dict:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(
                self.BASE_URL,
                params={
                    "parameters": parameters,
                    "community": "AG",
                    "longitude": longitude,
                    "latitude": latitude,
                    "start": start_date,
                    "end": end_date,
                    "format": "JSON"
                }
            )
            response.raise_for_status()
            return response.json()
```

### 2.2 ETL Pipeline Implementation

#### Data Pipeline Class
```python
# app/services/data_pipeline.py
from typing import Any, Dict
from app.services.connectors import UNHCRConnector, ACLEDConnector
from app.db.session import get_db
import pandas as pd

class DataPipeline:
    def __init__(self):
        self.unhcr = UNHCRConnector()
        self.acled = ACLEDConnector()
    
    async def extract(self, source: str, **kwargs) -> pd.DataFrame:
        """Extract data from source"""
        if source == "unhcr":
            data = await self.unhcr.fetch_population_data(**kwargs)
            return pd.DataFrame(data)
        elif source == "acled":
            data = await self.acled.fetch_events(**kwargs)
            return pd.DataFrame(data.get('data', []))
        else:
            raise ValueError(f"Unknown source: {source}")
    
    def transform(self, data: pd.DataFrame, source: str) -> pd.DataFrame:
        """Transform and clean data"""
        if source == "unhcr":
            return self._transform_unhcr(data)
        elif source == "acled":
            return self._transform_acled(data)
        return data
    
    def _transform_unhcr(self, df: pd.DataFrame) -> pd.DataFrame:
        # Standardize column names
        df = df.rename(columns={
            'Year': 'year',
            'Country of origin': 'origin_country',
            'Refugees': 'refugee_count'
        })
        # Handle missing values
        df = df.fillna(0)
        return df
    
    def _transform_acled(self, df: pd.DataFrame) -> pd.DataFrame:
        # Parse dates
        df['event_date'] = pd.to_datetime(df['event_date'])
        # Standardize location data
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        return df
    
    async def load(self, data: pd.DataFrame, table: str) -> bool:
        """Load data into database"""
        # Implementation depends on your ORM setup
        async with get_db() as db:
            # Use pandas to_sql or bulk insert
            # Example: data.to_sql(table, db.connection(), if_exists='append')
            pass
        return True
    
    def validate_quality(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Data quality checks"""
        report = {
            "total_rows": len(data),
            "missing_values": data.isnull().sum().to_dict(),
            "duplicates": data.duplicated().sum(),
            "columns": list(data.columns)
        }
        return report
```

### 2.3 Background Tasks with Celery

#### Celery Configuration
```python
# app/workers/celery_app.py
from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "migration_forecasting",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.task_routes = {
    "app.workers.data_tasks.*": "data-queue",
    "app.workers.training_tasks.*": "ml-queue"
}
```

#### Data Collection Tasks
```python
# app/workers/data_tasks.py
from app.workers.celery_app import celery_app
from app.services.data_pipeline import DataPipeline

@celery_app.task(bind=True)
def collect_unhcr_data(self, year: int):
    """Scheduled task to collect UNHCR data"""
    pipeline = DataPipeline()
    
    # Extract
    data = await pipeline.extract("unhcr", year=year)
    
    # Transform
    data = pipeline.transform(data, "unhcr")
    
    # Validate
    quality_report = pipeline.validate_quality(data)
    
    # Load
    success = await pipeline.load(data, "migration_events")
    
    return {"success": success, "quality": quality_report}

@celery_app.task
def update_conflict_data(country: str, days: int = 30):
    """Update conflict events for a country"""
    # Implementation
    pass
```

---

## Phase 3: ML Model Implementation

**Duration**: 4-6 weeks  
**Goal**: Implement and train ML models

### 3.1 Feature Engineering

```python
# app/ml/preprocessing/features.py
import pandas as pd
import numpy as np
from typing import List

class FeatureEngineering:
    def create_temporal_features(self, df: pd.DataFrame, date_col: str) -> pd.DataFrame:
        """Create time-based features"""
        df['year'] = df[date_col].dt.year
        df['month'] = df[date_col].dt.month
        df['quarter'] = df[date_col].dt.quarter
        df['day_of_year'] = df[date_col].dt.dayofyear
        return df
    
    def create_lag_features(
        self, 
        df: pd.DataFrame, 
        columns: List[str], 
        lags: List[int]
    ) -> pd.DataFrame:
        """Create lagged features for time series"""
        for col in columns:
            for lag in lags:
                df[f'{col}_lag_{lag}'] = df[col].shift(lag)
        return df
    
    def create_rolling_features(
        self,
        df: pd.DataFrame,
        column: str,
        windows: List[int]
    ) -> pd.DataFrame:
        """Create rolling statistics"""
        for window in windows:
            df[f'{column}_rolling_mean_{window}'] = df[column].rolling(window).mean()
            df[f'{column}_rolling_std_{window}'] = df[column].rolling(window).std()
        return df
    
    def create_spatial_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create spatial features from geographic data"""
        # Distance to borders, population density, etc.
        pass
```

### 3.2 Model Implementation

#### LSTM Model
```python
# app/ml/models/lstm.py
import torch
import torch.nn as nn

class GeoTemporalLSTM(nn.Module):
    def __init__(
        self, 
        input_dim: int,
        hidden_dim: int,
        num_layers: int,
        output_dim: int,
        dropout: float = 0.2
    ):
        super().__init__()
        
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        # LSTM layers
        self.lstm = nn.LSTM(
            input_dim,
            hidden_dim,
            num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )
        
        # Attention mechanism
        self.attention = nn.MultiheadAttention(hidden_dim, num_heads=4)
        
        # Output layer
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, output_dim)
        )
    
    def forward(self, x):
        # x shape: (batch, seq_len, features)
        lstm_out, (h_n, c_n) = self.lstm(x)
        
        # Apply attention
        attn_out, attn_weights = self.attention(
            lstm_out, lstm_out, lstm_out
        )
        
        # Use last hidden state
        output = self.fc(attn_out[:, -1, :])
        
        return output, attn_weights
```

#### Ensemble Model
```python
# app/ml/models/ensemble.py
from typing import List, Dict
import numpy as np
from app.ml.models.lstm import GeoTemporalLSTM
from xgboost import XGBRegressor

class MigrationEnsemble:
    def __init__(self):
        self.models = {
            'lstm': GeoTemporalLSTM(input_dim=50, hidden_dim=128, num_layers=2, output_dim=1),
            'xgboost': XGBRegressor(n_estimators=100, max_depth=6),
            'rf': RandomForestRegressor(n_estimators=100)
        }
        self.weights = {'lstm': 0.5, 'xgboost': 0.3, 'rf': 0.2}
    
    def predict_with_uncertainty(self, X: np.ndarray) -> Dict:
        predictions = []
        
        for name, model in self.models.items():
            pred = model.predict(X)
            predictions.append(pred * self.weights[name])
        
        # Ensemble prediction
        final_pred = np.sum(predictions, axis=0)
        
        # Uncertainty estimation (std of individual predictions)
        uncertainty = np.std([p / self.weights[name] for name, p in zip(self.models.keys(), predictions)], axis=0)
        
        return {
            'prediction': final_pred,
            'uncertainty': uncertainty,
            'lower_bound': final_pred - 1.96 * uncertainty,
            'upper_bound': final_pred + 1.96 * uncertainty
        }
```

### 3.3 Training Pipeline

```python
# app/ml/training/trainer.py
import torch
from torch.utils.data import DataLoader
from typing import Dict, Any
import optuna

class ModelTrainer:
    def __init__(self, model, config: Dict[str, Any]):
        self.model = model
        self.config = config
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
    
    def train(self, train_loader: DataLoader, val_loader: DataLoader):
        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.config['learning_rate'])
        criterion = torch.nn.MSELoss()
        
        best_val_loss = float('inf')
        
        for epoch in range(self.config['epochs']):
            # Training
            self.model.train()
            train_loss = 0
            for batch in train_loader:
                X, y = batch
                X, y = X.to(self.device), y.to(self.device)
                
                optimizer.zero_grad()
                predictions, _ = self.model(X)
                loss = criterion(predictions, y)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
            
            # Validation
            val_loss = self.evaluate(val_loader, criterion)
            
            # Save best model
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                self.save_checkpoint(f"best_model_epoch_{epoch}.pt")
            
            print(f"Epoch {epoch}: Train Loss: {train_loss/len(train_loader):.4f}, Val Loss: {val_loss:.4f}")
    
    def evaluate(self, data_loader: DataLoader, criterion) -> float:
        self.model.eval()
        total_loss = 0
        
        with torch.no_grad():
            for batch in data_loader:
                X, y = batch
                X, y = X.to(self.device), y.to(self.device)
                predictions, _ = self.model(X)
                loss = criterion(predictions, y)
                total_loss += loss.item()
        
        return total_loss / len(data_loader)
    
    def save_checkpoint(self, filename: str):
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'config': self.config
        }, f"data/models/{filename}")
```

---

## Phase 4: Frontend Development

**Duration**: 4-5 weeks  
**Goal**: Build interactive UI

### 4.1 Project Setup

```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install @mui/material @emotion/react @emotion/styled
npm install @reduxjs/toolkit react-redux
npm install react-router-dom
npm install mapbox-gl react-map-gl
npm install recharts d3
npm install axios
npm install react-hook-form zod
```

### 4.2 Core Components

#### Dashboard Component
```typescript
// src/components/Dashboard/Dashboard.tsx
import React, { useEffect } from 'react';
import { Grid, Card, CardContent, Typography } from '@mui/material';
import { useAppDispatch, useAppSelector } from '../../store/hooks';
import { fetchPredictions } from '../../store/slices/predictionSlice';
import TrendChart from './TrendChart';
import StatCard from './StatCard';

const Dashboard: React.FC = () => {
  const dispatch = useAppDispatch();
  const { predictions, loading } = useAppSelector(state => state.predictions);
  
  useEffect(() => {
    dispatch(fetchPredictions());
  }, [dispatch]);
  
  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={3}>
        <StatCard 
          title="Total Displaced"
          value="2.5M"
          change={+12.3}
        />
      </Grid>
      <Grid item xs={12} md={9}>
        <Card>
          <CardContent>
            <Typography variant="h6">Migration Trends</Typography>
            <TrendChart data={predictions} />
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
};

export default Dashboard;
```

#### Map Visualization
```typescript
// src/components/MapVisualization/MapContainer.tsx
import React, { useState } from 'react';
import Map, { Source, Layer } from 'react-map-gl';
import type { LayerProps } from 'react-map-gl';

const heatmapLayer: LayerProps = {
  id: 'heatmap',
  type: 'heatmap',
  paint: {
    'heatmap-weight': ['get', 'population'],
    'heatmap-intensity': 1,
    'heatmap-color': [
      'interpolate',
      ['linear'],
      ['heatmap-density'],
      0, 'rgba(0,0,255,0)',
      0.5, 'rgb(0,255,0)',
      1, 'rgb(255,0,0)'
    ]
  }
};

const MapContainer: React.FC = () => {
  const [viewState, setViewState] = useState({
    longitude: 20,
    latitude: 10,
    zoom: 2
  });
  
  return (
    <Map
      {...viewState}
      onMove={evt => setViewState(evt.viewState)}
      mapStyle="mapbox://styles/mapbox/light-v11"
      mapboxAccessToken={process.env.REACT_APP_MAPBOX_TOKEN}
    >
      <Source id="migration-data" type="geojson" data={migrationData}>
        <Layer {...heatmapLayer} />
      </Source>
    </Map>
  );
};
```

### 4.3 State Management

```typescript
// src/store/slices/predictionSlice.ts
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { predictionService } from '../../services/predictionService';

export const fetchPredictions = createAsyncThunk(
  'predictions/fetch',
  async (params: { region?: string; dateRange?: DateRange }) => {
    const response = await predictionService.getPredictions(params);
    return response.data;
  }
);

const predictionSlice = createSlice({
  name: 'predictions',
  initialState: {
    data: [],
    loading: false,
    error: null
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchPredictions.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchPredictions.fulfilled, (state, action) => {
        state.loading = false;
        state.data = action.payload;
      })
      .addCase(fetchPredictions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  }
});

export default predictionSlice.reducer;
```

---

## Phase 5: Advanced Features

### 5.1 Real-time Updates with WebSockets

```python
# Backend WebSocket endpoint
from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/predictions")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages
    except WebSocketDisconnect:
        manager.active_connections.remove(websocket)
```

### 5.2 Explainable AI Integration

```python
# app/ml/explainability/shap_explainer.py
import shap
import numpy as np

class SHAPExplainer:
    def __init__(self, model, background_data):
        self.explainer = shap.DeepExplainer(model, background_data)
    
    def explain_prediction(self, X: np.ndarray) -> dict:
        shap_values = self.explainer.shap_values(X)
        
        return {
            'shap_values': shap_values.tolist(),
            'base_value': self.explainer.expected_value,
            'feature_importance': np.abs(shap_values).mean(axis=0).tolist()
        }
```

---

## Development Workflow

### Local Development Setup
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Start services
docker-compose up -d  # PostgreSQL, Redis
```

### Git Workflow
1. Feature branches: `feature/feature-name`
2. Pull request reviews
3. CI/CD pipeline runs tests
4. Merge to main after approval

---

## Testing Strategy

### Backend Tests
```python
# tests/test_migration_service.py
import pytest
from app.services.migration_service import MigrationDataService

@pytest.mark.asyncio
async def test_ingest_unhcr_data():
    service = MigrationDataService()
    result = await service.ingest_unhcr_data(2023)
    assert result == True

@pytest.mark.asyncio
async def test_get_migration_trends():
    service = MigrationDataService()
    trends = await service.get_migration_trends("SOM", "yearly")
    assert len(trends) > 0
```

### Frontend Tests
```typescript
// src/components/Dashboard/Dashboard.test.tsx
import { render, screen } from '@testing-library/react';
import Dashboard from './Dashboard';

test('renders dashboard with stat cards', () => {
  render(<Dashboard />);
  expect(screen.getByText(/Total Displaced/i)).toBeInTheDocument();
});
```

---

**Last Updated**: 2025-10-13
