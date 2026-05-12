"""Service for orchestrating ensemble model training and prediction."""
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
import logging
from datetime import datetime
from app.ml.ensemble_model import EnsembleModel
from app.ml.models import LSTMModel, XGBoostModel, RandomForestModel
from app.services.training_service import LSTMTrainingService, XGBoostTrainingService, RandomForestTrainingService

logger = logging.getLogger(__name__)


class EnsembleService:
    """Service for training and using ensemble models."""

    def __init__(self):
        self.ensemble_model = EnsembleModel()
        self.lstm_trainer = LSTMTrainingService()
        self.xgboost_trainer = XGBoostTrainingService()
        self.rf_trainer = RandomForestTrainingService()
        logger.info("EnsembleService initialized")

    def train_ensemble(self,
                      X_lstm_train: np.ndarray, y_lstm_train: np.ndarray,
                      X_tabular_train: np.ndarray, y_tabular_train: np.ndarray,
                      X_lstm_val: np.ndarray = None, y_lstm_val: np.ndarray = None,
                      X_tabular_val: np.ndarray = None, y_tabular_val: np.ndarray = None,
                      lstm_params: Optional[Dict] = None,
                      xgb_params: Optional[Dict] = None,
                      rf_params: Optional[Dict] = None,
                      ensemble_weights: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Train the ensemble model by training all individual components.

        Args:
            X_lstm_train: Training sequences for LSTM
            y_lstm_train: Training targets for LSTM
            X_tabular_train: Training features for tree models
            y_tabular_train: Training targets for tree models
            X_lstm_val: Validation sequences for LSTM (optional)
            y_lstm_val: Validation targets for LSTM (optional)
            X_tabular_val: Validation features for tree models (optional)
            y_tabular_val: Validation targets for tree models (optional)
            lstm_params: Additional parameters for LSTM training
            xgb_params: Additional parameters for XGBoost training
            rf_params: Additional parameters for Random Forest training
            ensemble_weights: Weights for ensemble combination

        Returns:
            Dictionary containing training results
        """
        logger.info("Starting ensemble model training...")
        
        # Set ensemble weights if provided
        if ensemble_weights:
            self.ensemble_model.weights = ensemble_weights
            # Normalize weights
            total = sum(self.ensemble_model.weights.values())
            if total > 0:
                self.ensemble_model.weights = {k: v/total for k, v in self.ensemble_model.weights.items()}
        
        # Prepare kwargs for trainers
        lstm_kwargs = lstm_params or {}
        xgb_kwargs = xgb_params or {}
        rf_kwargs = rf_params or {}
        
        # Train individual models
        results = {}
        
        # Train LSTM
        logger.info("Training LSTM component...")
        try:
            lstm_result = self.lstm_trainer.train(
                X_lstm_train, y_lstm_train,
                X_val=X_lstm_val if X_lstm_val is not None else np.array([]),
                y_val=y_lstm_val if y_lstm_val is not None else np.array([]),
                **lstm_kwargs
            )
            # Get the trained LSTM model from the trainer
            self.ensemble_model.lstm_model = self.lstm_trainer.model
            results["lstm"] = lstm_result
            logger.info("LSTM training completed")
        except Exception as e:
            logger.error(f"LSTM training failed: {e}")
            results["lstm"] = {"error": str(e)}
        
        # Train XGBoost
        logger.info("Training XGBoost component...")
        try:
            xgb_result = self.xgboost_trainer.train(
                X_tabular_train, y_tabular_train,
                X_val=X_tabular_val if X_tabular_val is not None else np.array([]),
                y_val=y_tabular_val if y_tabular_val is not None else np.array([]),
                **xgb_kwargs
            )
            # Get the trained XGBoost model from the trainer
            self.ensemble_model.xgboost_model = self.xgboost_trainer.model
            results["xgboost"] = xgb_result
            logger.info("XGBoost training completed")
        except Exception as e:
            logger.error(f"XGBoost training failed: {e}")
            results["xgboost"] = {"error": str(e)}
        
        # Train Random Forest
        logger.info("Training Random Forest component...")
        try:
            rf_result = self.rf_trainer.train(
                X_tabular_train, y_tabular_train,
                X_val=X_tabular_val if X_tabular_val is not None else None,
                y_val=y_tabular_val if y_tabular_val is not None else None,
                **rf_kwargs
            )
            # Get the trained Random Forest model from the trainer
            self.ensemble_model.random_forest_model = self.rf_trainer.model
            results["random_forest"] = rf_result
            logger.info("Random Forest training completed")
        except Exception as e:
            logger.error(f"Random Forest training failed: {e}")
            results["random_forest"] = {"error": str(e)}
        
        # Mark ensemble as trained
        self.ensemble_model.is_trained = True
        
        # Evaluate ensemble on validation data if available
        if X_lstm_val is not None and X_tabular_val is not None and y_lstm_val is not None:
            logger.info("Evaluating ensemble on validation data...")
            try:
                ensemble_metrics = self.ensemble_model.evaluate(X_lstm_val, X_tabular_val, y_lstm_val)
                results["ensemble_validation"] = ensemble_metrics
                logger.info(f"Ensemble validation metrics: {ensemble_metrics}")
            except Exception as e:
                logger.error(f"Ensemble evaluation failed: {e}")
                results["ensemble_validation"] = {"error": str(e)}
        
        logger.info("Ensemble model training completed")
        return results

    def predict(self, X_lstm: np.ndarray, X_tabular: np.ndarray) -> np.ndarray:
        """
        Make predictions using the ensemble model.

        Args:
            X_lstm: Input data for LSTM model
            X_tabular: Input data for tree models

        Returns:
            Ensemble predictions
        """
        if not self.ensemble_model.is_trained:
            raise ValueError("Ensemble model is not trained. Call train_ensemble() first.")
        
        return self.ensemble_model.predict(X_lstm, X_tabular)

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
        if not self.ensemble_model.is_trained:
            raise ValueError("Ensemble model is not trained. Call train_ensemble() first.")
        
        return self.ensemble_model.evaluate(X_lstm, X_tabular, y_true)

    def save_ensemble(self, directory_path: str):
        """
        Save the ensemble model.

        Args:
            directory_path: Directory to save model components
        """
        self.ensemble_model.save(directory_path)
        logger.info(f"Ensemble model saved to {directory_path}")

    def load_ensemble(self, directory_path: str):
        """
        Load the ensemble model.

        Args:
            directory_path: Directory containing saved model components
        """
        self.ensemble_model.load(directory_path)
        logger.info(f"Ensemble model loaded from {directory_path}")

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the ensemble model and its components.

        Returns:
            Dictionary containing model information
        """
        info = {
            "ensemble_method": self.ensemble_model.ensemble_method,
            "weights": self.ensemble_model.weights,
            "is_trained": self.ensemble_model.is_trained,
            "components": {
                "lstm": {
                    "available": self.ensemble_model.lstm_model is not None,
                    "trained": self.ensemble_model.lstm_model.model is not None if self.ensemble_model.lstm_model else False
                },
                "xgboost": {
                    "available": self.ensemble_model.xgboost_model is not None,
                    "trained": self.ensemble_model.xgboost_model.model is not None if self.ensemble_model.xgboost_model else False
                },
                "random_forest": {
                    "available": self.ensemble_model.random_forest_model is not None,
                    "trained": self.ensemble_model.random_forest_model.model is not None if self.ensemble_model.random_forest_model else False
                }
            }
        }
        return info
