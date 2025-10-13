import numpy as np
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import joblib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.ml_models import MLModel, Prediction
from app.ml.models import LSTMModel, XGBoostModel, RandomForestModel

logger = logging.getLogger(__name__)


class ModelServing:
    """Service for loading and serving trained models."""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.loaded_models = {}  # Cache for loaded models
    
    async def get_active_model(
        self,
        model_type: str,
        country_iso: Optional[str] = None
    ) -> Optional[MLModel]:
        """
        Get active model from database.
        
        Args:
            model_type: Type of model (LSTM, XGBoost, RandomForest)
            country_iso: Country code (optional)
        
        Returns:
            MLModel instance or None
        """
        query = select(MLModel).where(
            MLModel.model_type == model_type,
            MLModel.is_active == True
        )
        
        if country_iso:
            query = query.where(MLModel.country_iso == country_iso)
        
        query = query.order_by(MLModel.created_at.desc())
        
        result = await self.db.execute(query)
        model = result.scalar_one_or_none()
        
        if model:
            logger.info(f"Found active {model_type} model: {model.name} (ID: {model.id})")
        else:
            logger.warning(f"No active {model_type} model found")
        
        return model
    
    def load_model(self, model_record: MLModel) -> Any:
        """
        Load model from disk.
        
        Args:
            model_record: MLModel database record
        
        Returns:
            Loaded model instance
        """
        cache_key = f"{model_record.model_type}_{model_record.id}"
        
        # Check cache
        if cache_key in self.loaded_models:
            logger.info(f"Using cached model: {cache_key}")
            return self.loaded_models[cache_key]
        
        # Load from disk
        logger.info(f"Loading model from {model_record.model_path}")
        
        if model_record.model_type == "LSTM":
            model = LSTMModel(
                sequence_length=model_record.hyperparameters.get("sequence_length", 12),
                n_features=model_record.n_features
            )
            model.load(model_record.model_path)
        
        elif model_record.model_type == "XGBoost":
            model = XGBoostModel()
            model.load(model_record.model_path)
        
        elif model_record.model_type == "RandomForest":
            model = RandomForestModel()
            model.load(model_record.model_path)
        
        else:
            raise ValueError(f"Unknown model type: {model_record.model_type}")
        
        # Cache model
        self.loaded_models[cache_key] = model
        return model
    
    def load_scaler(self, scaler_path: str):
        """Load preprocessing scaler."""
        return joblib.load(scaler_path)
    
    async def predict(
        self,
        model_type: str,
        features: np.ndarray,
        country_iso: Optional[str] = None,
        save_prediction: bool = True
    ) -> Dict[str, Any]:
        """
        Make prediction using active model.
        
        Args:
            model_type: Type of model
            features: Input features
            country_iso: Country code
            save_prediction: Whether to save prediction to database
        
        Returns:
            Prediction dict
        """
        # Get active model
        model_record = await self.get_active_model(model_type, country_iso)
        
        if not model_record:
            raise ValueError(f"No active {model_type} model found")
        
        # Load model
        model = self.load_model(model_record)
        
        # Make prediction
        prediction = model.predict(features)
        
        result = {
            "model_id": model_record.id,
            "model_name": model_record.name,
            "model_type": model_record.model_type,
            "predicted_value": float(prediction[0]) if isinstance(prediction, np.ndarray) else float(prediction),
            "country_iso": country_iso,
            "prediction_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        # Save to database if requested
        if save_prediction:
            pred_record = Prediction(
                model_id=model_record.id,
                country_iso=country_iso or "GLOBAL",
                prediction_date=result["prediction_date"],
                predicted_value=result["predicted_value"],
                input_features=features.tolist() if isinstance(features, np.ndarray) else features
            )
            self.db.add(pred_record)
            await self.db.commit()
            await self.db.refresh(pred_record)
            result["prediction_id"] = pred_record.id
        
        logger.info(f"Prediction: {result['predicted_value']:.2f}")
        return result
    
    async def batch_predict(
        self,
        model_type: str,
        features_list: List[np.ndarray],
        country_iso: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Make batch predictions.
        
        Args:
            model_type: Type of model
            features_list: List of feature arrays
            country_iso: Country code
        
        Returns:
            List of prediction dicts
        """
        # Get active model
        model_record = await self.get_active_model(model_type, country_iso)
        
        if not model_record:
            raise ValueError(f"No active {model_type} model found")
        
        # Load model
        model = self.load_model(model_record)
        
        # Stack features
        features_array = np.vstack(features_list)
        
        # Make predictions
        predictions = model.predict(features_array)
        
        results = []
        for i, pred in enumerate(predictions):
            result = {
                "model_id": model_record.id,
                "model_name": model_record.name,
                "model_type": model_record.model_type,
                "predicted_value": float(pred),
                "country_iso": country_iso,
                "index": i
            }
            results.append(result)
        
        logger.info(f"Batch prediction: {len(results)} predictions made")
        return results
    
    async def get_model_info(self, model_id: int) -> Dict[str, Any]:
        """Get model information."""
        result = await self.db.execute(
            select(MLModel).where(MLModel.id == model_id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            raise ValueError(f"Model not found: {model_id}")
        
        return {
            "id": model.id,
            "name": model.name,
            "model_type": model.model_type,
            "version": model.version,
            "country_iso": model.country_iso,
            "target_variable": model.target_variable,
            "n_features": model.n_features,
            "test_rmse": model.test_rmse,
            "test_mae": model.test_mae,
            "test_r2": model.test_r2,
            "status": model.status,
            "is_active": model.is_active,
            "created_at": model.created_at.isoformat(),
            "mlflow_run_id": model.mlflow_run_id
        }
    
    async def list_models(
        self,
        model_type: Optional[str] = None,
        country_iso: Optional[str] = None,
        active_only: bool = False
    ) -> List[Dict[str, Any]]:
        """List available models."""
        query = select(MLModel)
        
        if model_type:
            query = query.where(MLModel.model_type == model_type)
        
        if country_iso:
            query = query.where(MLModel.country_iso == country_iso)
        
        if active_only:
            query = query.where(MLModel.is_active == True)
        
        query = query.order_by(MLModel.created_at.desc())
        
        result = await self.db.execute(query)
        models = result.scalars().all()
        
        return [
            {
                "id": m.id,
                "name": m.name,
                "model_type": m.model_type,
                "version": m.version,
                "country_iso": m.country_iso,
                "test_rmse": m.test_rmse,
                "is_active": m.is_active,
                "created_at": m.created_at.isoformat()
            }
            for m in models
        ]
    
    async def activate_model(self, model_id: int) -> Dict[str, Any]:
        """Activate a model (deactivate others of same type)."""
        # Get model
        result = await self.db.execute(
            select(MLModel).where(MLModel.id == model_id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            raise ValueError(f"Model not found: {model_id}")
        
        # Deactivate other models of same type
        query = select(MLModel).where(
            MLModel.model_type == model.model_type,
            MLModel.is_active == True
        )
        
        if model.country_iso:
            query = query.where(MLModel.country_iso == model.country_iso)
        
        result = await self.db.execute(query)
        active_models = result.scalars().all()
        
        for m in active_models:
            m.is_active = False
        
        # Activate target model
        model.is_active = True
        model.status = "deployed"
        
        await self.db.commit()
        
        logger.info(f"Activated model {model_id}: {model.name}")
        return {"status": "success", "model_id": model_id, "model_name": model.name}
