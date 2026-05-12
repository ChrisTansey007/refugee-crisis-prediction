"""Ensemble model combining LSTM, XGBoost, and Random Forest for migration forecasting."""
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
import logging
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import joblib
import json
from datetime import datetime

from app.models.ml_models import LSTMModel, XGBoostModel, RandomForestModel

logger = logging.getLogger(__name__)


class EnsembleModel:
    """Ensemble model that combines multiple forecasting approaches."""

    def __init__(
        self,
        lstm_model: Optional[LSTMModel] = None,
        xgboost_model: Optional[XGBoostModel] = None,
        random_forest_model: Optional[RandomForestModel] = None,
        ensemble_method: str = "weighted_average",
        weights: Optional[Dict[str, float]] = None
    ):
        """
        Initialize ensemble model.

        Args:
            lstm_model: Trained LSTM model instance
            xgboost_model: Trained XGBoost model instance
            random_forest_model: Trained Random Forest model instance
            ensemble_method: Method for combining predictions ("weighted_average", "stacking")
            weights: Dictionary of model weights for weighted average
        """
        self.lstm_model = lstm_model
        self.xgboost_model = xgboost_model
        self.random_forest_model = random_forest_model
        self.ensemble_method = ensemble_method
        self.weights = weights or {
            "lstm": 0.4,
            "xgboost": 0.35,
            "random_forest": 0.25
        }
        self.is_trained = False
        
        # Validate weights sum to 1.0
        if abs(sum(self.weights.values()) - 1.0) > 0.001:
            logger.warning(f"Weights sum to {sum(self.weights.values())}, normalizing to 1.0")
            total = sum(self.weights.values())
            self.weights = {k: v/total for k, v in self.weights.items()}
            
        logger.info(f"EnsembleModel initialized with method: {ensemble_method}, weights: {self.weights}")

    def predict(self, X_lstm: np.ndarray, X_tabular: np.ndarray) -> np.ndarray:
        """
        Make predictions using the ensemble.

        Args:
            X_lstm: Input data for LSTM model (sequences)
            X_tabular: Input data for tree models (features)

        Returns:
            Ensemble predictions
        """
        if not self.is_trained:
            raise ValueError("Ensemble model is not trained. Call train() first or load pre-trained models.")

        predictions = {}
        weights_used = {}

        # Get LSTM predictions
        if self.lstm_model and self.lstm_model.model is not None:
            try:
                lstm_pred = self.lstm_model.predict(X_lstm)
                predictions["lstm"] = lstm_pred
                weights_used["lstm"] = self.weights.get("lstm", 0.0)
                logger.debug(f"LSTM predictions shape: {lstm_pred.shape}")
            except Exception as e:
                logger.warning(f"LSTM prediction failed: {e}")

        # Get XGBoost predictions
        if self.xgboost_model and self.xgboost_model.model is not None:
            try:
                xgb_pred = self.xgboost_model.predict(X_tabular)
                predictions["xgboost"] = xgb_pred
                weights_used["xgboost"] = self.weights.get("xgboost", 0.0)
                logger.debug(f"XGBoost predictions shape: {xgb_pred.shape}")
            except Exception as e:
                logger.warning(f"XGBoost prediction failed: {e}")

        # Get Random Forest predictions
        if self.random_forest_model and self.random_forest_model.model is not None:
            try:
                rf_pred = self.random_forest_model.predict(X_tabular)
                predictions["random_forest"] = rf_pred
                weights_used["random_forest"] = self.weights.get("random_forest", 0.0)
                logger.debug(f"Random Forest predictions shape: {rf_pred.shape}")
            except Exception as e:
                logger.warning(f"Random Forest prediction failed: {e}")

        if not predictions:
            raise ValueError("No models available for prediction")

        # Combine predictions based on ensemble method
        if self.ensemble_method == "weighted_average":
            return self._weighted_average_predictions(predictions, weights_used)
        elif self.ensemble_method == "stacking":
            # For now, fall back to weighted average as stacking would require a meta-model
            logger.warning("Stacking method not fully implemented, falling back to weighted average")
            return self._weighted_average_predictions(predictions, weights_used)
        else:
            raise ValueError(f"Unknown ensemble method: {self.ensemble_method}")

    def _weighted_average_predictions(self, predictions: Dict[str, np.ndarray], weights: Dict[str, float]) -> np.ndarray:
        """Combine predictions using weighted average."""
        # Ensure we have the same number of predictions for each model
        pred_arrays = list(predictions.values())
        if not pred_arrays:
            raise ValueError("No predictions to combine")
            
        # Check all predictions have same shape
        first_shape = pred_arrays[0].shape
        for i, pred in enumerate(pred_arrays[1:], 1):
            if pred.shape != first_shape:
                raise ValueError(f"Prediction shape mismatch: {list(predictions.keys())[0]} has shape {first_shape}, "
                               f"but {list(predictions.keys())[i]} has shape {pred.shape}")

        # Weighted average
        weighted_sum = np.zeros_like(pred_arrays[0])
        total_weight = 0.0
        
        for model_name, pred in predictions.items():
            weight = weights.get(model_name, 0.0)
            weighted_sum += weight * pred
            total_weight += weight

        # Normalize by total weight (in case weights don't sum to 1 due to missing models)
        if total_weight > 0:
            weighted_sum = weighted_sum / total_weight
            
        logger.debug(f"Ensemble prediction shape: {weighted_sum.shape}")
        return weighted_sum

    def evaluate(self, X_lstm: np.ndarray, X_tabular: np.ndarray, y_true: np.ndarray) -> Dict[str, float]:
        """
        Evaluate ensemble performance.

        Args:
            X_lstm: Input data for LSTM model
            X_tabular: Input data for tree models
            y_true: True target values

        Returns:
            Dictionary of evaluation metrics
        """
        y_pred = self.predict(X_lstm, X_tabular)
        
        metrics = {
            "mse": float(mean_squared_error(y_true, y_pred)),
            "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
            "mae": float(mean_absolute_error(y_true, y_pred)),
            "r2": float(r2_score(y_true, y_pred))
        }
        
        logger.info(f"Ensemble Test Metrics: RMSE={metrics['rmse']:.4f}, MAE={metrics['mae']:.4f}, R2={metrics['r2']:.4f}")
        return metrics

    def save(self, directory_path: str):
        """
        Save ensemble model and components.

        Args:
            directory_path: Directory to save model components
        """
        import os
        os.makedirs(directory_path, exist_ok=True)
        
        # Save individual models if they exist
        if self.lstm_model and self.lstm_model.model is not None:
            lstm_path = os.path.join(directory_path, "lstm_model")
            self.lstm_model.save(lstm_path)
            
        if self.xgboost_model and self.xgboost_model.model is not None:
            xgb_path = os.path.join(directory_path, "xgboost_model.json")
            self.xgboost_model.save(xgb_path)
            
        if self.random_forest_model and self.random_forest_model.model is not None:
            rf_path = os.path.join(directory_path, "random_forest_model.joblib")
            self.random_forest_model.save(rf_path)
        
        # Save ensemble metadata
        ensemble_metadata = {
            "ensemble_method": self.ensemble_method,
            "weights": self.weights,
            "is_trained": self.is_trained,
            "saved_at": datetime.now().isoformat(),
            "components": {
                "lstm": self.lstm_model is not None and self.lstm_model.model is not None,
                "xgboost": self.xgboost_model is not None and self.xgboost_model.model is not None,
                "random_forest": self.random_forest_model is not None and self.random_forest_model.model is not None
            }
        }
        
        metadata_path = os.path.join(directory_path, "ensemble_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(ensemble_metadata, f, indent=2)
            
        logger.info(f"Ensemble model saved to {directory_path}")

    def load(self, directory_path: str):
        """
        Load ensemble model and components.

        Args:
            directory_path: Directory containing saved model components
        """
        import os
        
        # Load individual models if they exist
        lstm_path = os.path.join(directory_path, "lstm_model")
        if os.path.exists(lstm_path):
            if not self.lstm_model:
                self.lstm_model = LSTMModel(sequence_length=10, n_features=5)  # Default values
            self.lstm_model.load(lstm_path)
            logger.info(f"Loaded LSTM model from {lstm_path}")
            
        xgb_path = os.path.join(directory_path, "xgboost_model.json")
        if os.path.exists(xgb_path):
            if not self.xgboost_model:
                self.xgboost_model = XGBoostModel()
            self.xgboost_model.load(xgb_path)
            logger.info(f"Loaded XGBoost model from {xgb_path}")
            
        rf_path = os.path.join(directory_path, "random_forest_model.joblib")
        if os.path.exists(rf_path):
            if not self.random_forest_model:
                self.random_forest_model = RandomForestModel()
            self.random_forest_model.load(rf_path)
            logger.info(f"Loaded Random Forest model from {rf_path}")
        
        # Load ensemble metadata
        metadata_path = os.path.join(directory_path, "ensemble_metadata.json")
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                ensemble_metadata = json.load(f)
            self.ensemble_method = ensemble_metadata.get("ensemble_method", self.ensemble_method)
            self.weights = ensemble_metadata.get("weights", self.weights)
            self.is_trained = ensemble_metadata.get("is_trained", False)
            logger.info(f"Loaded ensemble metadata from {metadata_path}")
        else:
            # If no metadata, assume we need to set is_trained based on loaded models
            self.is_trained = (
                (self.lstm_model and self.lstm_model.model is not None) or
                (self.xgboost_model and self.xgboost_model.model is not None) or
                (self.random_forest_model and self.random_forest_model.model is not None)
            )
            logger.warning("No ensemble metadata found, setting is_trained based on loaded models")

    def train_individual_models(self, 
                              X_lstm_train: np.ndarray, y_lstm_train: np.ndarray,
                              X_tabular_train: np.ndarray, y_tabular_train: np.ndarray,
                              X_lstm_val: np.ndarray = None, y_lstm_val: np.ndarray = None,
                              X_tabular_val: np.ndarray = None, y_tabular_val: np.ndarray = None,
                              **kwargs) -> Dict[str, Any]:
        """
        Train all individual models in the ensemble.

        Args:
            X_lstm_train: Training sequences for LSTM
            y_lstm_train: Training targets for LSTM
            X_tabular_train: Training features for tree models
            y_tabular_train: Training targets for tree models
            X_lstm_val: Validation sequences for LSTM (optional)
            y_lstm_val: Validation targets for LSTM (optional)
            X_tabular_val: Validation features for tree models (optional)
            y_tabular_val: Validation targets for tree models (optional)
            **kwargs: Additional arguments passed to individual model training

        Returns:
            Dictionary containing training results for each model
        """
        results = {}
        
        # Train LSTM model
        if self.lstm_model:
            logger.info("Training LSTM model...")
            try:
                lstm_result = self.lstm_model.train(
                    X_lstm_train, y_lstm_train,
                    X_val=X_lstm_val if X_lstm_val is not None else np.array([]),
                    y_val=y_lstm_val if y_lstm_val is not None else np.array([]),
                    **kwargs
                )
                results["lstm"] = lstm_result
                logger.info("LSTM model training completed")
            except Exception as e:
                logger.error(f"LSTM model training failed: {e}")
                results["lstm"] = {"error": str(e)}
        
        # Train XGBoost model
        if self.xgboost_model:
            logger.info("Training XGBoost model...")
            try:
                xgb_result = self.xgboost_model.train(
                    X_tabular_train, y_tabular_train,
                    X_val=X_tabular_val if X_tabular_val is not None else np.array([]),
                    y_val=y_tabular_val if y_tabular_val is not None else np.array([]),
                    **kwargs
                )
                results["xgboost"] = xgb_result
                logger.info("XGBoost model training completed")
            except Exception as e:
                logger.error(f"XGBoost model training failed: {e}")
                results["xgboost"] = {"error": str(e)}
        
        # Train Random Forest model
        if self.random_forest_model:
            logger.info("Training Random Forest model...")
            try:
                rf_result = self.random_forest_model.train(
                    X_tabular_train, y_tabular_train,
                    X_val=X_tabular_val if X_tabular_val is not None else None,
                    y_val=y_tabular_val if y_tabular_val is not None else None,
                    **kwargs
                )
                results["random_forest"] = rf_result
                logger.info("Random Forest model training completed")
            except Exception as e:
                logger.error(f"Random Forest model training failed: {e}")
                results["random_forest"] = {"error": str(e)}
        
        self.is_trained = True
        logger.info("All individual models training completed")
        return results
