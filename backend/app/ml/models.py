import numpy as np
import logging
from typing import Dict, Any, Optional, Tuple
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import mlflow
import mlflow.sklearn
import mlflow.xgboost
import mlflow.keras

logger = logging.getLogger(__name__)


class LSTMModel:
    """LSTM model for time series forecasting."""
    
    def __init__(
        self,
        sequence_length: int,
        n_features: int,
        lstm_units: int = 64,
        dropout_rate: float = 0.2,
        learning_rate: float = 0.001
    ):
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.lstm_units = lstm_units
        self.dropout_rate = dropout_rate
        self.learning_rate = learning_rate
        self.model = None
        self.history = None
    
    def build_model(self) -> keras.Model:
        """Build LSTM model architecture."""
        model = keras.Sequential([
            layers.LSTM(
                self.lstm_units,
                activation='tanh',
                return_sequences=True,
                input_shape=(self.sequence_length, self.n_features)
            ),
            layers.Dropout(self.dropout_rate),
            layers.LSTM(self.lstm_units // 2, activation='tanh'),
            layers.Dropout(self.dropout_rate),
            layers.Dense(32, activation='relu'),
            layers.Dense(1)
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate),
            loss='mse',
            metrics=['mae']
        )
        
        self.model = model
        logger.info(f"Built LSTM model: {self.lstm_units} units, {self.dropout_rate} dropout")
        return model
    
    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        epochs: int = 100,
        batch_size: int = 32,
        early_stopping_patience: int = 10
    ) -> Dict[str, Any]:
        """
        Train LSTM model.
        
        Args:
            X_train: Training sequences (samples, timesteps, features)
            y_train: Training targets
            X_val: Validation sequences
            y_val: Validation targets
            epochs: Maximum number of epochs
            batch_size: Batch size
            early_stopping_patience: Patience for early stopping
        
        Returns:
            Training history dict
        """
        if self.model is None:
            self.build_model()
        
        # Callbacks
        early_stopping = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=early_stopping_patience,
            restore_best_weights=True
        )
        
        reduce_lr = keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-6
        )
        
        # Train
        logger.info(f"Training LSTM for up to {epochs} epochs")
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping, reduce_lr],
            verbose=0
        )
        
        logger.info(f"Training completed in {len(self.history.history['loss'])} epochs")
        return self.history.history
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions."""
        return self.model.predict(X, verbose=0).flatten()
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """Evaluate model on test set."""
        y_pred = self.predict(X_test)
        
        metrics = {
            "mse": float(mean_squared_error(y_test, y_pred)),
            "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
            "mae": float(mean_absolute_error(y_test, y_pred)),
            "r2": float(r2_score(y_test, y_pred))
        }
        
        logger.info(f"LSTM Test Metrics: RMSE={metrics['rmse']:.4f}, MAE={metrics['mae']:.4f}, R2={metrics['r2']:.4f}")
        return metrics
    
    def save(self, filepath: str):
        """Save model to file."""
        self.model.save(filepath)
        logger.info(f"Saved LSTM model to {filepath}")
    
    def load(self, filepath: str):
        """Load model from file."""
        self.model = keras.models.load_model(filepath)
        logger.info(f"Loaded LSTM model from {filepath}")


class XGBoostModel:
    """XGBoost model for regression."""
    
    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: int = 6,
        learning_rate: float = 0.1,
        subsample: float = 0.8,
        colsample_bytree: float = 0.8
    ):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.learning_rate = learning_rate
        self.subsample = subsample
        self.colsample_bytree = colsample_bytree
        self.model = None
    
    def build_model(self) -> xgb.XGBRegressor:
        """Build XGBoost model."""
        self.model = xgb.XGBRegressor(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            learning_rate=self.learning_rate,
            subsample=self.subsample,
            colsample_bytree=self.colsample_bytree,
            random_state=42,
            n_jobs=-1
        )
        logger.info(f"Built XGBoost model: {self.n_estimators} trees, depth={self.max_depth}")
        return self.model
    
    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        early_stopping_rounds: int = 10
    ) -> Dict[str, Any]:
        """Train XGBoost model."""
        if self.model is None:
            self.build_model()
        
        logger.info("Training XGBoost model")
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            early_stopping_rounds=early_stopping_rounds,
            verbose=False
        )
        
        logger.info(f"Training completed with {self.model.best_iteration} iterations")
        return {"best_iteration": self.model.best_iteration}
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions."""
        return self.model.predict(X)
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """Evaluate model on test set."""
        y_pred = self.predict(X_test)
        
        metrics = {
            "mse": float(mean_squared_error(y_test, y_pred)),
            "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
            "mae": float(mean_absolute_error(y_test, y_pred)),
            "r2": float(r2_score(y_test, y_pred))
        }
        
        logger.info(f"XGBoost Test Metrics: RMSE={metrics['rmse']:.4f}, MAE={metrics['mae']:.4f}, R2={metrics['r2']:.4f}")
        return metrics
    
    def get_feature_importance(self, feature_names: list) -> Dict[str, float]:
        """Get feature importance scores."""
        importance = self.model.feature_importances_
        return dict(zip(feature_names, importance.tolist()))
    
    def save(self, filepath: str):
        """Save model to file."""
        self.model.save_model(filepath)
        logger.info(f"Saved XGBoost model to {filepath}")
    
    def load(self, filepath: str):
        """Load model from file."""
        self.model = xgb.XGBRegressor()
        self.model.load_model(filepath)
        logger.info(f"Loaded XGBoost model from {filepath}")


class RandomForestModel:
    """Random Forest baseline model."""
    
    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: Optional[int] = None,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1
    ):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.model = None
    
    def build_model(self) -> RandomForestRegressor:
        """Build Random Forest model."""
        self.model = RandomForestRegressor(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            min_samples_split=self.min_samples_split,
            min_samples_leaf=self.min_samples_leaf,
            random_state=42,
            n_jobs=-1
        )
        logger.info(f"Built Random Forest model: {self.n_estimators} trees")
        return self.model
    
    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray = None,
        y_val: np.ndarray = None
    ) -> Dict[str, Any]:
        """Train Random Forest model."""
        if self.model is None:
            self.build_model()
        
        logger.info("Training Random Forest model")
        self.model.fit(X_train, y_train)
        
        logger.info("Training completed")
        return {"n_estimators": self.n_estimators}
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions."""
        return self.model.predict(X)
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """Evaluate model on test set."""
        y_pred = self.predict(X_test)
        
        metrics = {
            "mse": float(mean_squared_error(y_test, y_pred)),
            "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
            "mae": float(mean_absolute_error(y_test, y_pred)),
            "r2": float(r2_score(y_test, y_pred))
        }
        
        logger.info(f"Random Forest Test Metrics: RMSE={metrics['rmse']:.4f}, MAE={metrics['mae']:.4f}, R2={metrics['r2']:.4f}")
        return metrics
    
    def get_feature_importance(self, feature_names: list) -> Dict[str, float]:
        """Get feature importance scores."""
        importance = self.model.feature_importances_
        return dict(zip(feature_names, importance.tolist()))
    
    def save(self, filepath: str):
        """Save model to file."""
        import joblib
        joblib.dump(self.model, filepath)
        logger.info(f"Saved Random Forest model to {filepath}")
    
    def load(self, filepath: str):
        """Load model from file."""
        import joblib
        self.model = joblib.load(filepath)
        logger.info(f"Loaded Random Forest model from {filepath}")
