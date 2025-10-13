import pandas as pd
import numpy as np
from typing import Tuple, Dict, List, Optional
from datetime import datetime
import logging
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import joblib

logger = logging.getLogger(__name__)


class DatasetPreparation:
    """Prepare datasets for ML model training with temporal splits."""
    
    def __init__(self):
        self.scaler = None
        self.feature_columns = None
        self.target_column = None
    
    def create_sequences(
        self,
        data: np.ndarray,
        sequence_length: int,
        forecast_horizon: int = 1
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create sequences for time series forecasting.
        
        Args:
            data: Input data array
            sequence_length: Number of time steps to look back
            forecast_horizon: Number of time steps to forecast ahead
        
        Returns:
            Tuple of (X, y) arrays
        """
        X, y = [], []
        
        for i in range(len(data) - sequence_length - forecast_horizon + 1):
            X.append(data[i:i + sequence_length])
            y.append(data[i + sequence_length + forecast_horizon - 1])
        
        return np.array(X), np.array(y)
    
    def temporal_train_test_split(
        self,
        df: pd.DataFrame,
        test_size: float = 0.2,
        validation_size: float = 0.1
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Split data temporally (no shuffling to prevent data leakage).
        
        Args:
            df: Input DataFrame sorted by date
            test_size: Proportion for test set
            validation_size: Proportion for validation set
        
        Returns:
            Tuple of (train_df, val_df, test_df)
        """
        n = len(df)
        test_idx = int(n * (1 - test_size))
        val_idx = int(test_idx * (1 - validation_size))
        
        train_df = df.iloc[:val_idx].copy()
        val_df = df.iloc[val_idx:test_idx].copy()
        test_df = df.iloc[test_idx:].copy()
        
        logger.info(f"Split: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}")
        return train_df, val_df, test_df
    
    def prepare_features_and_target(
        self,
        df: pd.DataFrame,
        target_column: str,
        feature_columns: Optional[List[str]] = None,
        exclude_columns: Optional[List[str]] = None
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Separate features and target variable.
        
        Args:
            df: Input DataFrame
            target_column: Name of target column
            feature_columns: List of feature columns (if None, use all except target)
            exclude_columns: Columns to exclude from features
        
        Returns:
            Tuple of (X, y)
        """
        if exclude_columns is None:
            exclude_columns = ["date"]
        
        if feature_columns is None:
            # Use all columns except target and excluded
            feature_columns = [
                col for col in df.columns 
                if col != target_column and col not in exclude_columns
            ]
        
        X = df[feature_columns].copy()
        y = df[target_column].copy()
        
        self.feature_columns = feature_columns
        self.target_column = target_column
        
        logger.info(f"Features: {len(feature_columns)}, Target: {target_column}")
        return X, y
    
    def scale_features(
        self,
        X_train: pd.DataFrame,
        X_val: pd.DataFrame,
        X_test: pd.DataFrame,
        method: str = "standard"
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Scale features using training set statistics.
        
        Args:
            X_train: Training features
            X_val: Validation features
            X_test: Test features
            method: Scaling method ('standard' or 'minmax')
        
        Returns:
            Tuple of scaled (X_train, X_val, X_test)
        """
        if method == "standard":
            self.scaler = StandardScaler()
        elif method == "minmax":
            self.scaler = MinMaxScaler()
        else:
            raise ValueError(f"Unknown scaling method: {method}")
        
        # Fit on training data only
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        X_test_scaled = self.scaler.transform(X_test)
        
        logger.info(f"Scaled features using {method} scaler")
        return X_train_scaled, X_val_scaled, X_test_scaled
    
    def prepare_lstm_dataset(
        self,
        df: pd.DataFrame,
        target_column: str,
        sequence_length: int = 12,
        forecast_horizon: int = 1,
        test_size: float = 0.2,
        validation_size: float = 0.1,
        feature_columns: Optional[List[str]] = None
    ) -> Dict:
        """
        Prepare complete dataset for LSTM training.
        
        Args:
            df: Input DataFrame
            target_column: Target variable name
            sequence_length: Number of time steps to look back
            forecast_horizon: Number of time steps to forecast
            test_size: Test set proportion
            validation_size: Validation set proportion
            feature_columns: Feature columns to use
        
        Returns:
            Dict with train/val/test splits and metadata
        """
        logger.info("Preparing LSTM dataset")
        
        # Temporal split
        train_df, val_df, test_df = self.temporal_train_test_split(
            df, test_size, validation_size
        )
        
        # Prepare features and target
        X_train, y_train = self.prepare_features_and_target(
            train_df, target_column, feature_columns
        )
        X_val, y_val = self.prepare_features_and_target(
            val_df, target_column, self.feature_columns
        )
        X_test, y_test = self.prepare_features_and_target(
            test_df, target_column, self.feature_columns
        )
        
        # Scale features
        X_train_scaled, X_val_scaled, X_test_scaled = self.scale_features(
            X_train, X_val, X_test, method="minmax"
        )
        
        # Create sequences
        X_train_seq, y_train_seq = self.create_sequences(
            X_train_scaled, sequence_length, forecast_horizon
        )
        X_val_seq, y_val_seq = self.create_sequences(
            X_val_scaled, sequence_length, forecast_horizon
        )
        X_test_seq, y_test_seq = self.create_sequences(
            X_test_scaled, sequence_length, forecast_horizon
        )
        
        # Reshape for LSTM (samples, timesteps, features)
        n_features = X_train_scaled.shape[1]
        X_train_seq = X_train_seq.reshape(X_train_seq.shape[0], sequence_length, n_features)
        X_val_seq = X_val_seq.reshape(X_val_seq.shape[0], sequence_length, n_features)
        X_test_seq = X_test_seq.reshape(X_test_seq.shape[0], sequence_length, n_features)
        
        # Extract target column index for y
        target_idx = self.feature_columns.index(target_column)
        y_train_seq = y_train_seq[:, target_idx]
        y_val_seq = y_val_seq[:, target_idx]
        y_test_seq = y_test_seq[:, target_idx]
        
        logger.info(f"LSTM dataset prepared: X_train shape={X_train_seq.shape}")
        
        return {
            "X_train": X_train_seq,
            "y_train": y_train_seq,
            "X_val": X_val_seq,
            "y_val": y_val_seq,
            "X_test": X_test_seq,
            "y_test": y_test_seq,
            "scaler": self.scaler,
            "feature_columns": self.feature_columns,
            "target_column": self.target_column,
            "sequence_length": sequence_length,
            "n_features": n_features
        }
    
    def prepare_tabular_dataset(
        self,
        df: pd.DataFrame,
        target_column: str,
        test_size: float = 0.2,
        validation_size: float = 0.1,
        feature_columns: Optional[List[str]] = None
    ) -> Dict:
        """
        Prepare dataset for tabular models (XGBoost, RandomForest).
        
        Args:
            df: Input DataFrame
            target_column: Target variable name
            test_size: Test set proportion
            validation_size: Validation set proportion
            feature_columns: Feature columns to use
        
        Returns:
            Dict with train/val/test splits and metadata
        """
        logger.info("Preparing tabular dataset")
        
        # Temporal split
        train_df, val_df, test_df = self.temporal_train_test_split(
            df, test_size, validation_size
        )
        
        # Prepare features and target
        X_train, y_train = self.prepare_features_and_target(
            train_df, target_column, feature_columns
        )
        X_val, y_val = self.prepare_features_and_target(
            val_df, target_column, self.feature_columns
        )
        X_test, y_test = self.prepare_features_and_target(
            test_df, target_column, self.feature_columns
        )
        
        # Scale features
        X_train_scaled, X_val_scaled, X_test_scaled = self.scale_features(
            X_train, X_val, X_test, method="standard"
        )
        
        logger.info(f"Tabular dataset prepared: X_train shape={X_train_scaled.shape}")
        
        return {
            "X_train": X_train_scaled,
            "y_train": y_train.values,
            "X_val": X_val_scaled,
            "y_val": y_val.values,
            "X_test": X_test_scaled,
            "y_test": y_test.values,
            "scaler": self.scaler,
            "feature_columns": self.feature_columns,
            "target_column": self.target_column
        }
    
    def save_preprocessing_artifacts(self, filepath: str):
        """Save scaler and feature metadata."""
        artifacts = {
            "scaler": self.scaler,
            "feature_columns": self.feature_columns,
            "target_column": self.target_column
        }
        joblib.dump(artifacts, filepath)
        logger.info(f"Saved preprocessing artifacts to {filepath}")
    
    def load_preprocessing_artifacts(self, filepath: str):
        """Load scaler and feature metadata."""
        artifacts = joblib.load(filepath)
        self.scaler = artifacts["scaler"]
        self.feature_columns = artifacts["feature_columns"]
        self.target_column = artifacts["target_column"]
        logger.info(f"Loaded preprocessing artifacts from {filepath}")
    
    def check_data_leakage(self, train_df: pd.DataFrame, test_df: pd.DataFrame) -> Dict:
        """
        Check for potential data leakage between train and test sets.
        
        Args:
            train_df: Training DataFrame
            test_df: Test DataFrame
        
        Returns:
            Dict with leakage check results
        """
        results = {
            "temporal_order_ok": True,
            "no_overlap": True,
            "messages": []
        }
        
        # Check temporal order
        if "date" in train_df.columns and "date" in test_df.columns:
            train_max_date = train_df["date"].max()
            test_min_date = test_df["date"].min()
            
            if train_max_date >= test_min_date:
                results["temporal_order_ok"] = False
                results["messages"].append(
                    f"Temporal leakage: Train max date ({train_max_date}) >= Test min date ({test_min_date})"
                )
        
        # Check for duplicate rows
        train_set = set(train_df.index)
        test_set = set(test_df.index)
        overlap = train_set.intersection(test_set)
        
        if overlap:
            results["no_overlap"] = False
            results["messages"].append(f"Index overlap: {len(overlap)} rows")
        
        if results["temporal_order_ok"] and results["no_overlap"]:
            results["messages"].append("No data leakage detected")
        
        return results
