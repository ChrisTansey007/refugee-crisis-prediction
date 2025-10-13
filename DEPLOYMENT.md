# Deployment & Operations Guide

## Table of Contents
- [Infrastructure Setup](#infrastructure-setup)
- [Docker Configuration](#docker-configuration)
- [Cloud Deployment](#cloud-deployment)
- [Monitoring & Observability](#monitoring--observability)
- [Security & Compliance](#security--compliance)
- [Backup & Recovery](#backup--recovery)
- [Performance Optimization](#performance-optimization)

---

## Infrastructure Setup

### Local Development Environment

#### Prerequisites
```bash
# Install Docker & Docker Compose
docker --version  # Should be 24.0+
docker-compose --version  # Should be 2.20+

# Install Node.js and Python
node --version  # Should be 20+
python --version  # Should be 3.11+
```

#### Environment Configuration
```bash
# Create .env files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Edit configuration
nano backend/.env
nano frontend/.env
```

---

## Docker Configuration

### docker-compose.yml (Development)

```yaml
version: '3.8'

services:
  # PostgreSQL with PostGIS
  db:
    image: postgis/postgis:15-3.4
    container_name: migration_db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: migration_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - migration_network

  # Redis
  redis:
    image: redis:7-alpine
    container_name: migration_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - migration_network

  # Backend API
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: migration_api
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
      - ./data:/app/data
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/migration_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    networks:
      - migration_network

  # Celery Worker
  worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: migration_worker
    command: celery -A app.workers.celery_app worker --loglevel=info
    volumes:
      - ./backend:/app
      - ./data:/app/data
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/migration_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    networks:
      - migration_network

  # Celery Beat (Scheduler)
  scheduler:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: migration_scheduler
    command: celery -A app.workers.celery_app beat --loglevel=info
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/migration_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    networks:
      - migration_network

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    container_name: migration_frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://localhost:8000
    networks:
      - migration_network

volumes:
  postgres_data:
  redis_data:

networks:
  migration_network:
    driver: bridge
```

### Backend Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    libpq-dev \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create data directories
RUN mkdir -p data/raw data/processed data/models

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

```dockerfile
# frontend/Dockerfile
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### nginx.conf

```nginx
server {
    listen 80;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/css application/javascript application/json image/svg+xml;
    gzip_min_length 1000;

    # API proxy
    location /api {
        proxy_pass http://api:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # WebSocket support
    location /ws {
        proxy_pass http://api:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # React routing
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

---

## Cloud Deployment

### AWS Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Route 53 (DNS)                       │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│              CloudFront (CDN) + WAF                     │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│           Application Load Balancer (ALB)               │
└──────┬─────────────────────────────────────┬────────────┘
       │                                     │
       ▼                                     ▼
┌─────────────────┐                  ┌─────────────────┐
│  ECS/Fargate    │                  │   S3 Bucket     │
│  (API Service)  │                  │  (Static Files) │
└────────┬────────┘                  └─────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│              RDS PostgreSQL (Multi-AZ)                  │
│              + ElastiCache Redis                        │
└─────────────────────────────────────────────────────────┘
```

### AWS ECS Task Definition

```json
{
  "family": "migration-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "your-ecr-repo/migration-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://..."
        }
      ],
      "secrets": [
        {
          "name": "SECRET_KEY",
          "valueFrom": "arn:aws:secretsmanager:..."
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/migration-api",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "api"
        }
      }
    }
  ]
}
```

### Terraform Configuration (Sample)

```hcl
# main.tf
provider "aws" {
  region = "us-east-1"
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "migration-vpc"
  }
}

# RDS PostgreSQL
resource "aws_db_instance" "postgres" {
  identifier           = "migration-db"
  engine               = "postgres"
  engine_version       = "15.3"
  instance_class       = "db.t3.medium"
  allocated_storage    = 100
  storage_encrypted    = true
  
  db_name  = "migration_db"
  username = var.db_username
  password = var.db_password
  
  multi_az               = true
  backup_retention_period = 7
  
  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  tags = {
    Name = "migration-postgres"
  }
}

# ElastiCache Redis
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "migration-redis"
  engine               = "redis"
  node_type            = "cache.t3.medium"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
  
  subnet_group_name    = aws_elasticache_subnet_group.main.name
  security_group_ids   = [aws_security_group.redis.id]
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "migration-cluster"
}

# ECS Service
resource "aws_ecs_service" "api" {
  name            = "migration-api"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = 2
  launch_type     = "FARGATE"
  
  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.api.id]
    assign_public_ip = false
  }
  
  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "api"
    container_port   = 8000
  }
}
```

### Kubernetes Deployment (Alternative)

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: migration-api
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: migration-api
  template:
    metadata:
      labels:
        app: migration-api
    spec:
      containers:
      - name: api
        image: your-registry/migration-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: migration-api-service
  namespace: production
spec:
  type: LoadBalancer
  selector:
    app: migration-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

---

## Monitoring & Observability

### Prometheus Metrics

```python
# app/core/metrics.py
from prometheus_client import Counter, Histogram, Gauge
from prometheus_fastapi_instrumentator import Instrumentator

# Custom metrics
prediction_counter = Counter(
    'migration_predictions_total',
    'Total number of predictions made'
)

prediction_latency = Histogram(
    'migration_prediction_duration_seconds',
    'Time spent generating predictions'
)

model_accuracy = Gauge(
    'migration_model_accuracy',
    'Current model accuracy score',
    ['model_name']
)

# Initialize instrumentation
instrumentator = Instrumentator()

@app.on_event("startup")
async def startup():
    instrumentator.instrument(app).expose(app)
```

### Logging Configuration

```python
# app/core/logging.py
import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

logger = setup_logging()
```

### Grafana Dashboard Configuration

```json
{
  "dashboard": {
    "title": "Migration Forecasting System",
    "panels": [
      {
        "title": "API Request Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Prediction Latency",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, migration_prediction_duration_seconds_bucket)"
          }
        ]
      },
      {
        "title": "Model Accuracy",
        "targets": [
          {
            "expr": "migration_model_accuracy"
          }
        ]
      }
    ]
  }
}
```

### Alert Rules

```yaml
# alerts.yml
groups:
  - name: migration_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} requests/sec"
      
      - alert: DatabaseConnectionPoolExhausted
        expr: db_connections_active / db_connections_max > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Database connection pool nearly exhausted"
      
      - alert: ModelAccuracyDegraded
        expr: migration_model_accuracy < 0.7
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Model accuracy has degraded"
```

---

## Security & Compliance

### Security Best Practices

#### 1. Environment Variables
```bash
# Never commit secrets to git
# Use secret management services

# AWS Secrets Manager
aws secretsmanager create-secret \
  --name migration-db-password \
  --secret-string "your-secure-password"

# Access in application
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']
```

#### 2. API Security
```python
# app/core/security.py
from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/v1/predictions")
@limiter.limit("10/minute")
async def get_predictions():
    pass
```

#### 3. Database Security
```sql
-- Create read-only user for analytics
CREATE USER analytics_reader WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE migration_db TO analytics_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytics_reader;

-- Row-level security
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_predictions ON predictions
  FOR SELECT
  USING (user_id = current_user_id());
```

### GDPR Compliance

```python
# app/services/gdpr_service.py
class GDPRService:
    async def export_user_data(self, user_id: str) -> bytes:
        """Export all user data (Right to Data Portability)"""
        # Collect all user data
        user_data = await self.collect_user_data(user_id)
        # Return as JSON
        return json.dumps(user_data).encode()
    
    async def delete_user_data(self, user_id: str) -> bool:
        """Delete user data (Right to Erasure)"""
        # Anonymize or delete user records
        await self.anonymize_user_records(user_id)
        return True
    
    async def anonymize_user_records(self, user_id: str):
        """Anonymize user data while retaining analytics value"""
        # Replace identifiable information with anonymized data
        pass
```

---

## Backup & Recovery

### Database Backup Strategy

```bash
# Automated daily backups
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/postgres"
DB_NAME="migration_db"

# Create backup
pg_dump -h localhost -U postgres -d $DB_NAME | gzip > "$BACKUP_DIR/backup_$DATE.sql.gz"

# Upload to S3
aws s3 cp "$BACKUP_DIR/backup_$DATE.sql.gz" "s3://your-backup-bucket/postgres/"

# Keep only last 30 days
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete
```

### Disaster Recovery Plan

```yaml
# RTO (Recovery Time Objective): 4 hours
# RPO (Recovery Point Objective): 1 hour

Recovery Steps:
  1. Detect Failure:
     - Monitoring alerts trigger
     - Verify scope of failure
  
  2. Initiate Recovery:
     - Switch to backup region (if multi-region)
     - Restore database from latest backup
     - Verify data integrity
  
  3. Application Recovery:
     - Deploy application containers
     - Update DNS records
     - Verify all services operational
  
  4. Post-Recovery:
     - Analyze root cause
     - Update runbooks
     - Communicate with stakeholders
```

---

## Performance Optimization

### Database Optimization

```sql
-- Create indexes
CREATE INDEX CONCURRENTLY idx_migration_events_date 
  ON migration_events(event_date);

CREATE INDEX CONCURRENTLY idx_predictions_region_date 
  ON predictions(region_id, target_date);

-- Spatial indexes
CREATE INDEX idx_regions_geometry 
  ON regions USING GIST(geometry);

-- Partitioning for large tables
CREATE TABLE migration_events_2024 PARTITION OF migration_events
  FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

-- Analyze tables
ANALYZE migration_events;
ANALYZE predictions;

-- Vacuum
VACUUM ANALYZE;
```

### Caching Strategy

```python
# app/utils/cache.py
from functools import wraps
import redis
import json
from typing import Callable

redis_client = redis.Redis.from_url(settings.REDIS_URL)

def cache_result(expire: int = 3600):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            
            # Check cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Cache result
            redis_client.setex(
                cache_key,
                expire,
                json.dumps(result)
            )
            
            return result
        return wrapper
    return decorator

# Usage
@cache_result(expire=1800)
async def get_predictions(region_id: str):
    # Expensive operation
    pass
```

### API Performance

```python
# Enable compression
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Connection pooling
from sqlalchemy.pool import QueuePool

engine = create_async_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True
)

# Async batch operations
async def batch_predict(regions: List[str]):
    tasks = [generate_prediction(region) for region in regions]
    results = await asyncio.gather(*tasks)
    return results
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          cd backend
          pytest --cov=app tests/
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Build and push image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/migration-api:$IMAGE_TAG backend/
          docker push $ECR_REGISTRY/migration-api:$IMAGE_TAG

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster migration-cluster \
            --service migration-api \
            --force-new-deployment
```

---

## Maintenance & Operations

### Scheduled Maintenance Tasks

```python
# Celery scheduled tasks
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    'daily-data-refresh': {
        'task': 'app.workers.data_tasks.refresh_all_data',
        'schedule': crontab(hour=2, minute=0),  # 2 AM daily
    },
    'weekly-model-retrain': {
        'task': 'app.workers.training_tasks.retrain_models',
        'schedule': crontab(day_of_week=1, hour=3, minute=0),  # Monday 3 AM
    },
    'hourly-prediction-update': {
        'task': 'app.workers.prediction_tasks.update_predictions',
        'schedule': crontab(minute=0),  # Every hour
    }
}
```

### Health Checks

```python
@app.get("/health")
async def health_check():
    checks = {
        "api": "healthy",
        "database": await check_database(),
        "redis": await check_redis(),
        "models": await check_models_loaded()
    }
    
    if all(v == "healthy" for v in checks.values()):
        return {"status": "healthy", "checks": checks}
    else:
        raise HTTPException(status_code=503, detail=checks)
```

---

**Last Updated**: 2025-10-13
