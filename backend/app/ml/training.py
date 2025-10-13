import mlflow
import mlflow.sklearn
import mlflow.xgboost
import mlflow.keras
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import numpy as np
from app.ml.models import LSTMModel, XGBoostModel, RandomForestModel
from app.ml.dataset import DatasetPreparation

logger = logging.getLogger(__name__)


class ModelTrainer:
    """Orchestrate model training with MLflow tracking."""
    
    def __init__(self, experiment_name: str = "migration_forecasting"):
        self.experiment_name = experiment_name
        mlflow.set_experiment(experiment_name)
        logger.info(f"MLflow experiment: {experiment_name}")
    
    def train_lstm(
        self,
        dataset: Dict[str, Any],
        lstm_units: int = 64,
        dropout_rate: float = 0.2,
        learning_rate: float = 0.001,
        epochs: int = 100,
        batch_size: int = 32
    ) -> Dict[str, Any]:
        """
        Train LSTM model with MLflow tracking.
        
        Args:
            dataset: Dataset dict from DatasetPreparation.prepare_lstm_dataset()
            lstm_units: Number of LSTM units
            dropout_rate: Dropout rate
            learning_rate: Learning rate
            epochs: Maximum epochs
            batch_size: Batch size
        
        Returns:
            Dict with model, metrics, and run_id
        """
        with mlflow.start_run(run_name=f"LSTM_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
            # Log parameters
            mlflow.log_params({
                "model_type": "LSTM",
                "lstm_units": lstm_units,
                "dropout_rate": dropout_rate,
                "learning_rate": learning_rate,
                "epochs": epochs,
                "batch_size": batch_size,
                "sequence_length": dataset["sequence_length"],
                "n_features": dataset["n_features"]
            })
            
            # Build and train model
            model = LSTMModel(
                sequence_length=dataset["sequence_length"],
                n_features=dataset["n_features"],
                lstm_units=lstm_units,
                dropout_rate=dropout_rate,
                learning_rate=learning_rate
            )
            
            history = model.train(
                X_train=dataset["X_train"],
                y_train=dataset["y_train"],
                X_val=dataset["X_val"],
                y_val=dataset["y_val"],
                epochs=epochs,
                batch_size=batch_size
            )
            
            # Log training metrics
            for epoch, (loss, val_loss) in enumerate(zip(history["loss"], history["val_loss"])):
                mlflow.log_metrics({"train_loss": loss, "val_loss": val_loss}, step=epoch)
            
            # Evaluate on test set
            test_metrics = model.evaluate(dataset["X_test"], dataset["y_test"])
            mlflow.log_metrics({
                "test_rmse": test_metrics["rmse"],
                "test_mae": test_metrics["mae"],
                "test_r2": test_metrics["r2"]
            })
            
            # Log model
            mlflow.keras.log_model(model.model, "model")
            
            run_id = mlflow.active_run().info.run_id
            logger.info(f"LSTM training completed. Run ID: {run_id}")
            
            return {
                "model": model,
                "metrics": test_metrics,
                "history": history,
                "run_id": run_id
            }
    
    def train_xgboost(
        self,
        dataset: Dict[str, Any],
        n_estimators: int = 100,
        max_depth: int = 6,
        learning_rate: float = 0.1,
        subsample: float = 0.8,
        colsample_bytree: float = 0.8
    ) -> Dict[str, Any]:
        """
        Train XGBoost model with MLflow tracking.
        
        Args:
            dataset: Dataset dict from DatasetPreparation.prepare_tabular_dataset()
            n_estimators: Number of trees
            max_depth: Maximum tree depth
            learning_rate: Learning rate
            subsample: Subsample ratio
            colsample_bytree: Column subsample ratio
        
        Returns:
            Dict with model, metrics, and run_id
        """
        with mlflow.start_run(run_name=f"XGBoost_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
            # Log parameters
            mlflow.log_params({
                "model_type": "XGBoost",
                "n_estimators": n_estimators,
                "max_depth": max_depth,
                "learning_rate": learning_rate,
                "subsample": subsample,
                "colsample_bytree": colsample_bytree,
                "n_features": len(dataset["feature_columns"])
            })
            
            # Build and train model
            model = XGBoostModel(
                n_estimators=n_estimators,
                max_depth=max_depth,
                learning_rate=learning_rate,
                subsample=subsample,
                colsample_bytree=colsample_bytree
            )
            
            model.train(
                X_train=dataset["X_train"],
                y_train=dataset["y_train"],
                X_val=dataset["X_val"],
                y_val=dataset["y_val"]
            )
            
            # Evaluate on test set
            test_metrics = model.evaluate(dataset["X_test"], dataset["y_test"])
            mlflow.log_metrics({
                "test_rmse": test_metrics["rmse"],
                "test_mae": test_metrics["mae"],
                "test_r2": test_metrics["r2"]
            })
            
            # Log feature importance
            feature_importance = model.get_feature_importance(dataset["feature_columns"])
            top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:10]
            for feat, imp in top_features:
                mlflow.log_metric(f"importance_{feat}", imp)
            
            # Log model
            mlflow.xgboost.log_model(model.model, "model")
            
            run_id = mlflow.active_run().info.run_id
            logger.info(f"XGBoost training completed. Run ID: {run_id}")
            
            return {
                "model": model,
                "metrics": test_metrics,
                "feature_importance": feature_importance,
                "run_id": run_id
            }
    
    def train_random_forest(
        self,
        dataset: Dict[str, Any],
        n_estimators: int = 100,
        max_depth: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Train Random Forest baseline with MLflow tracking.
        
        Args:
            dataset: Dataset dict from DatasetPreparation.prepare_tabular_dataset()
            n_estimators: Number of trees
            max_depth: Maximum tree depth
        
        Returns:
            Dict with model, metrics, and run_id
        """
        with mlflow.start_run(run_name=f"RandomForest_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
            # Log parameters
            mlflow.log_params({
                "model_type": "RandomForest",
                "n_estimators": n_estimators,
                "max_depth": max_depth,
                "n_features": len(dataset["feature_columns"])
            })
            
            # Build and train model
            model = RandomForestModel(
                n_estimators=n_estimators,
                max_depth=max_depth
            )
            
            model.train(
                X_train=dataset["X_train"],
                y_train=dataset["y_train"]
            )
            
            # Evaluate on test set
            test_metrics = model.evaluate(dataset["X_test"], dataset["y_test"])
            mlflow.log_metrics({
                "test_rmse": test_metrics["rmse"],
                "test_mae": test_metrics["mae"],
                "test_r2": test_metrics["r2"]
            })
            
            # Log feature importance
            feature_importance = model.get_feature_importance(dataset["feature_columns"])
            top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:10]
            for feat, imp in top_features:
                mlflow.log_metric(f"importance_{feat}", imp)
            
            # Log model
            mlflow.sklearn.log_model(model.model, "model")
            
            run_id = mlflow.active_run().info.run_id
            logger.info(f"Random Forest training completed. Run ID: {run_id}")
            
            return {
                "model": model,
                "metrics": test_metrics,
                "feature_importance": feature_importance,
                "run_id": run_id
            }
    
    def compare_models(
        self,
        lstm_result: Dict[str, Any],
        xgboost_result: Dict[str, Any],
        rf_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compare model performance.
        
        Args:
            lstm_result: LSTM training result
            xgboost_result: XGBoost training result
            rf_result: Random Forest training result
        
        Returns:
            Comparison dict with best model
        """
        models = {
            "LSTM": lstm_result["metrics"],
            "XGBoost": xgboost_result["metrics"],
            "RandomForest": rf_result["metrics"]
        }
        
        # Find best model by RMSE
        best_model = min(models.items(), key=lambda x: x[1]["rmse"])
        
        comparison = {
            "models": models,
            "best_model": {
                "name": best_model[0],
                "rmse": best_model[1]["rmse"],
                "mae": best_model[1]["mae"],
                "r2": best_model[1]["r2"]
            }
        }
        
        logger.info(f"Best model: {best_model[0]} with RMSE={best_model[1]['rmse']:.4f}")
        return comparison
