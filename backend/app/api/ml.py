from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from pydantic import BaseModel
import numpy as np
from app.core.database import get_db
from app.ml.features import FeatureEngineering
from app.ml.serving import ModelServing
from app.ml.explainability import ModelExplainer

router = APIRouter(prefix="/api/v1/ml", tags=["Machine Learning"])


class FeatureExtractionRequest(BaseModel):
    country_iso: str
    start_date: str  # YYYY-MM-DD
    end_date: str  # YYYY-MM-DD
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class DatasetCreationRequest(BaseModel):
    country_iso: str
    start_date: str
    end_date: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@router.post("/features/displacement")
async def extract_displacement_features(
    request: FeatureExtractionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Extract displacement features for a country.
    
    Example:
    ```json
    {
        "country_iso": "AFG",
        "start_date": "2015-01-01",
        "end_date": "2023-12-31"
    }
    ```
    """
    try:
        fe = FeatureEngineering(db)
        df = await fe.extract_displacement_features(
            country_iso=request.country_iso,
            start_date=request.start_date,
            end_date=request.end_date
        )
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No data found")
        
        return {
            "status": "success",
            "rows": len(df),
            "columns": list(df.columns),
            "sample": df.head(5).to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/features/economic")
async def extract_economic_features(
    request: FeatureExtractionRequest,
    db: AsyncSession = Depends(get_db)
):
    """Extract economic indicator features for a country."""
    try:
        fe = FeatureEngineering(db)
        df = await fe.extract_economic_features(
            country_iso=request.country_iso,
            start_date=request.start_date,
            end_date=request.end_date
        )
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No data found")
        
        return {
            "status": "success",
            "rows": len(df),
            "columns": list(df.columns),
            "sample": df.head(5).to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/features/conflict")
async def extract_conflict_features(
    request: FeatureExtractionRequest,
    db: AsyncSession = Depends(get_db)
):
    """Extract conflict event features for a country."""
    try:
        fe = FeatureEngineering(db)
        df = await fe.extract_conflict_features(
            country_iso=request.country_iso,
            start_date=request.start_date,
            end_date=request.end_date
        )
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No data found")
        
        return {
            "status": "success",
            "rows": len(df),
            "columns": list(df.columns),
            "sample": df.head(5).to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/dataset/create")
async def create_ml_dataset(
    request: DatasetCreationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Create complete ML dataset by merging all feature sources.
    
    Example:
    ```json
    {
        "country_iso": "AFG",
        "start_date": "2015-01-01",
        "end_date": "2023-12-31",
        "latitude": 33.9,
        "longitude": 67.7
    }
    ```
    """
    try:
        fe = FeatureEngineering(db)
        df = await fe.create_ml_dataset(
            country_iso=request.country_iso,
            start_date=request.start_date,
            end_date=request.end_date,
            latitude=request.latitude,
            longitude=request.longitude
        )
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No data found")
        
        return {
            "status": "success",
            "rows": len(df),
            "columns": len(df.columns),
            "feature_list": list(df.columns),
            "date_range": {
                "start": str(df["date"].min()),
                "end": str(df["date"].max())
            },
            "sample": df.head(5).to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Model Serving Endpoints

class PredictionRequest(BaseModel):
    model_type: str  # LSTM, XGBoost, RandomForest
    features: List[List[float]]  # 2D array of features
    country_iso: Optional[str] = None


class ModelActivationRequest(BaseModel):
    model_id: int


@router.post("/predict")
async def make_prediction(
    request: PredictionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Make prediction using active model.
    
    Example:
    ```json
    {
        "model_type": "XGBoost",
        "features": [[100, 50, 25, 10, 5, 1.5, 2.3]],
        "country_iso": "AFG"
    }
    ```
    """
    try:
        serving = ModelServing(db)
        features_array = np.array(request.features)
        
        result = await serving.predict(
            model_type=request.model_type,
            features=features_array,
            country_iso=request.country_iso
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
async def list_models(
    model_type: Optional[str] = None,
    country_iso: Optional[str] = None,
    active_only: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """
    List available models.
    
    Query parameters:
    - model_type: Filter by model type (LSTM, XGBoost, RandomForest)
    - country_iso: Filter by country
    - active_only: Show only active models
    """
    try:
        serving = ModelServing(db)
        models = await serving.list_models(
            model_type=model_type,
            country_iso=country_iso,
            active_only=active_only
        )
        return {"models": models, "count": len(models)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/{model_id}")
async def get_model_info(
    model_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information about a specific model."""
    try:
        serving = ModelServing(db)
        info = await serving.get_model_info(model_id)
        return info
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/models/activate")
async def activate_model(
    request: ModelActivationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Activate a model for serving (deactivates others of same type).
    
    Example:
    ```json
    {
        "model_id": 5
    }
    ```
    """
    try:
        serving = ModelServing(db)
        result = await serving.activate_model(request.model_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Explainability Endpoints

class ExplainRequest(BaseModel):
    model_id: int
    features: List[List[float]]  # Test features
    feature_names: List[str]
    max_display: int = 10


class ExplainSingleRequest(BaseModel):
    model_id: int
    features: List[float]  # Single instance
    feature_names: List[str]


@router.post("/explain/global")
async def explain_model_global(
    request: ExplainRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Get global model explanation using SHAP.
    
    Example:
    ```json
    {
        "model_id": 5,
        "features": [[100, 50, 25], [120, 55, 30]],
        "feature_names": ["refugees", "gdp", "conflicts"],
        "max_display": 10
    }
    ```
    """
    try:
        serving = ModelServing(db)
        
        # Get model
        model_info = await serving.get_model_info(request.model_id)
        model_record = await serving.get_active_model(
            model_type=model_info["model_type"]
        )
        model = serving.load_model(model_record)
        
        # Create explainer
        explainer = ModelExplainer()
        X_test = np.array(request.features)
        
        # Get explanation based on model type
        if model_info["model_type"] == "XGBoost":
            explanation = explainer.explain_xgboost(
                model, X_test, request.feature_names, request.max_display
            )
        elif model_info["model_type"] == "RandomForest":
            explanation = explainer.explain_random_forest(
                model, X_test, request.feature_names, request.max_display
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Explainability not supported for {model_info['model_type']}"
            )
        
        return {
            "model_id": request.model_id,
            "model_type": model_info["model_type"],
            "explanation": explanation
        }
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain/single")
async def explain_single_prediction(
    request: ExplainSingleRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Explain a single prediction using SHAP.
    
    Example:
    ```json
    {
        "model_id": 5,
        "features": [100, 50, 25, 10, 5],
        "feature_names": ["refugees", "gdp", "conflicts", "temp", "precip"]
    }
    ```
    """
    try:
        serving = ModelServing(db)
        
        # Get model
        model_info = await serving.get_model_info(request.model_id)
        model_record = await serving.get_active_model(
            model_type=model_info["model_type"]
        )
        model = serving.load_model(model_record)
        
        # Create explainer
        explainer = ModelExplainer()
        X_instance = np.array(request.features)
        
        # Get explanation
        explanation = explainer.explain_single_prediction(
            model,
            X_instance,
            request.feature_names,
            model_type=model_info["model_type"].lower()
        )
        
        return {
            "model_id": request.model_id,
            "model_type": model_info["model_type"],
            "explanation": explanation
        }
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/{model_id}/feature-importance")
async def get_feature_importance(
    model_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get native feature importance from model."""
    try:
        serving = ModelServing(db)
        
        # Get model
        model_info = await serving.get_model_info(model_id)
        model_record = await serving.get_active_model(
            model_type=model_info["model_type"]
        )
        model = serving.load_model(model_record)
        
        # Get feature importance
        explainer = ModelExplainer()
        importance = explainer.get_feature_importance_native(
            model,
            model_info["feature_list"],
            model_type=model_info["model_type"].lower()
        )
        
        # Sort by importance
        sorted_importance = sorted(
            importance.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            "model_id": model_id,
            "model_type": model_info["model_type"],
            "feature_importance": dict(sorted_importance[:20]),
            "top_features": [f[0] for f in sorted_importance[:10]]
        }
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
