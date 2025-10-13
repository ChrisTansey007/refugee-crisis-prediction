# Migration Forecasting System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18.0+-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104+-009688.svg)](https://fastapi.tiangolo.com/)

A comprehensive AI-powered platform for predicting forced migration patterns using multi-modal spatiotemporal data. This system leverages machine learning, geospatial analysis, and real-time data integration to provide early warning signals for humanitarian crises.

## 🎯 Project Overview

The Migration Forecasting System combines:
- **Machine Learning**: Deep learning models (LSTM, CNN) and ensemble methods
- **Geospatial Analysis**: PostGIS-powered spatial operations and mapping
- **Real-time Data**: Integration with 15+ free data sources (UNHCR, ACLED, NASA, World Bank)
- **Interactive UI**: React-based dashboard with advanced visualizations

**Key Capabilities:**
- Predict migration flows 4-26 weeks in advance
- Analyze climate, conflict, and economic indicators
- Generate explainable AI insights with SHAP values
- Visualize predictions on interactive maps

---

## 📚 Documentation

This project documentation is organized into specialized guides:

### **[📊 DATA_SOURCES.md](./DATA_SOURCES.md)**
Comprehensive guide to all free data sources and APIs
- UNHCR Refugee Statistics API
- ACLED Conflict Data
- NASA Climate Data (POWER API)
- World Bank Economic Indicators
- WorldPop Population Data
- Sentinel/Landsat Satellite Imagery
- GDELT Global Events
- Complete API documentation with examples

### **[🏗️ ARCHITECTURE.md](./ARCHITECTURE.md)**
System design and technology stack
- High-level architecture diagrams
- Backend structure (FastAPI, PostgreSQL, Redis)
- Frontend structure (React, TypeScript, Redux)
- Database schema design
- ML pipeline architecture
- Complete technology stack

### **[⚙️ IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)**
Step-by-step development guide
- Phase 1: Backend Core Infrastructure
- Phase 2: Data Integration Layer
- Phase 3: ML Model Implementation
- Phase 4: Frontend Development
- Phase 5: Advanced Features
- Code examples and best practices

### **[🚀 DEPLOYMENT.md](./DEPLOYMENT.md)**
Deployment and operations guide
- Docker configuration
- AWS/Cloud deployment
- Kubernetes setup
- Monitoring & observability
- Security & compliance
- Backup & disaster recovery

### **[☁️ DEPLOYMENT_RENDER.md](./DEPLOYMENT_RENDER.md)**
Render deployment (Docker-free)
- Render architecture & services
- `render.yaml` blueprint
- Required environment variables
- Static site + Python web service + worker/cron

---

## 🚀 Quick Start

### Prerequisites
```bash
- Python 3.11+ (for local development)
- Node.js 20+ (for local development)
# Optional (for local containers; NOT required for Render):
- Docker 24.0+
- Docker Compose 2.20+
```

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/refugee-crisis-prediction.git
   cd refugee-crisis-prediction
   ```

2. **Set up environment variables**
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   # Edit .env files with your configuration
   ```

3. **Start all services with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Initialize the database**
   ```bash
   docker-compose exec api alembic upgrade head
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Manual Setup (Without Docker)

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## ☁️ Deploy on Render (Summary)
- Connect your GitHub repo in Render
- Use `render.yaml` (Render Blueprint) or follow `DEPLOYMENT_RENDER.md`
- Create Managed PostgreSQL and Redis (use INTERNAL URLs)
- Create services:
  - Web Service (FastAPI): `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
  - Worker (Celery): `celery -A app.workers.celery_app worker --loglevel=info`
  - (Optional) Beat or Cron for scheduled jobs
  - Static Site (frontend): `npm ci && npm run build` → `dist`
- Set env vars: `DATABASE_URL`, `REDIS_URL`, `SECRET_KEY`, `LOG_LEVEL`, `VITE_API_URL`

See full guide: [DEPLOYMENT_RENDER.md](./DEPLOYMENT_RENDER.md)

---

## 🏗️ Project Structure

```
refugee-crisis-prediction/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration
│   │   ├── models/         # Database models
│   │   ├── ml/             # ML models & training
│   │   ├── services/       # Business logic
│   │   └── workers/        # Celery tasks
│   ├── data/               # Data storage
│   └── tests/              # Backend tests
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── store/         # Redux store
│   │   └── utils/         # Utilities
│   └── tests/             # Frontend tests
│
├── docs/                   # Additional documentation
├── scripts/                # Utility scripts
├── docker-compose.yml      # Optional: local containers
├── render.yaml             # Render blueprint (optional)
├── DATA_SOURCES.md         # Data sources guide
├── ARCHITECTURE.md         # Architecture documentation
├── IMPLEMENTATION_GUIDE.md # Development guide
├── DEPLOYMENT.md           # Docker/K8s deployment guide
└── DEPLOYMENT_RENDER.md    # Render deployment guide
```

---

## 🔑 Key Features

### 🤖 Machine Learning
- **Deep Learning Models**: GeoTemporalLSTM with attention mechanisms
- **Ensemble Methods**: Combining LSTM, XGBoost, and Random Forest
- **Uncertainty Quantification**: Confidence intervals and prediction bands
- **Explainable AI**: SHAP values and feature importance visualization

### 📊 Data Integration
- **15+ Data Sources**: Automated ingestion from UNHCR, ACLED, NASA, World Bank
- **ETL Pipeline**: Extract, transform, load with data quality validation
- **Real-time Updates**: Celery workers for scheduled data collection
- **Geospatial Processing**: PostGIS for spatial queries and analysis

### 🗺️ Interactive Visualization
- **Dynamic Maps**: Mapbox-powered interactive maps with multiple layers
- **Time-series Charts**: Recharts and D3.js visualizations
- **Prediction Explorer**: What-if analysis and scenario planning
- **Model Comparison**: Side-by-side model performance metrics

### 🔐 Security & Compliance
- **Authentication**: JWT-based secure authentication
- **GDPR Compliance**: Data export and erasure capabilities
- **Rate Limiting**: API protection and abuse prevention
- **Encryption**: Data encryption at rest and in transit

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest --cov=app tests/
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:e2e  # Playwright E2E tests
```

---

## 📈 Performance

- **API Response Time**: <500ms for predictions
- **Prediction Lead Time**: 4-26 weeks ahead
- **System Uptime**: 99.9% availability target
- **Data Freshness**: Daily updates for most sources

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](./CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

### Data Providers
- **UNHCR** - Refugee statistics and operational data
- **ACLED** - Armed Conflict Location & Event Data
- **NASA** - Climate and satellite data
- **World Bank** - Economic indicators
- **WorldPop** - Population data
- **GDELT** - Global events database

### Technology Partners
- FastAPI, PyTorch, React, Material-UI
- PostgreSQL, PostGIS, Redis
- Docker, Kubernetes

---

## 📧 Contact

- **Project Lead**: [Your Name](mailto:your.email@example.com)
- **Issues**: [GitHub Issues](https://github.com/yourusername/refugee-crisis-prediction/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/refugee-crisis-prediction/discussions)

---

## 🗺️ Roadmap

### Current Phase: Foundation (v0.1)
- ✅ System architecture design
- ✅ Data source identification
- 🔄 Backend core infrastructure
- 🔄 Database schema implementation

### Phase 2: Data Integration (v0.2)
- ⏳ API connectors for all data sources
- ⏳ ETL pipeline implementation
- ⏳ Data quality validation

### Phase 3: ML Models (v0.3)
- ⏳ LSTM model implementation
- ⏳ Ensemble model development
- ⏳ Training pipeline setup

### Phase 4: Frontend (v0.4)
- ⏳ Dashboard development
- ⏳ Map visualization
- ⏳ Model management interface

### Phase 5: Production (v1.0)
- ⏳ Cloud deployment
- ⏳ Monitoring & alerting
- ⏳ Performance optimization

---

## 📊 Project Status

![Project Progress](https://img.shields.io/badge/Progress-Planning%20Phase-blue)
![Build Status](https://img.shields.io/badge/Build-Not%20Started-lightgrey)
![Documentation](https://img.shields.io/badge/Documentation-Complete-green)

**Last Updated**: 2025-10-13

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐
