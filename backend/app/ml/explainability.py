import numpy as np
import shap
import logging
from typing import Dict, Any, List, Optional
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import io
import base64

logger = logging.getLogger(__name__)


class ModelExplainer:
    """Model explainability using SHAP and feature importance."""
    
    def __init__(self):
        self.explainer = None
        self.shap_values = None
    
    def explain_xgboost(
        self,
        model,
        X_test: np.ndarray,
        feature_names: List[str],
        max_display: int = 10
    ) -> Dict[str, Any]:
        """
        Explain XGBoost model predictions using SHAP.
        
        Args:
            model: Trained XGBoost model
            X_test: Test features
            feature_names: List of feature names
            max_display: Maximum features to display
        
        Returns:
            Dict with SHAP values and visualizations
        """
        logger.info("Computing SHAP values for XGBoost model")
        
        # Create explainer
        self.explainer = shap.TreeExplainer(model.model)
        
        # Calculate SHAP values
        self.shap_values = self.explainer.shap_values(X_test)
        
        # Get feature importance (mean absolute SHAP values)
        feature_importance = np.abs(self.shap_values).mean(axis=0)
        importance_dict = dict(zip(feature_names, feature_importance.tolist()))
        
        # Sort by importance
        sorted_importance = sorted(
            importance_dict.items(),
            key=lambda x: x[1],
            reverse=True
        )[:max_display]
        
        # Generate summary plot
        summary_plot = self._create_summary_plot(
            self.shap_values,
            X_test,
            feature_names,
            max_display
        )
        
        logger.info(f"SHAP analysis complete. Top feature: {sorted_importance[0][0]}")
        
        return {
            "feature_importance": dict(sorted_importance),
            "shap_values_shape": self.shap_values.shape,
            "summary_plot": summary_plot,
            "top_features": [f[0] for f in sorted_importance]
        }
    
    def explain_random_forest(
        self,
        model,
        X_test: np.ndarray,
        feature_names: List[str],
        max_display: int = 10
    ) -> Dict[str, Any]:
        """
        Explain Random Forest model predictions using SHAP.
        
        Args:
            model: Trained Random Forest model
            X_test: Test features
            feature_names: List of feature names
            max_display: Maximum features to display
        
        Returns:
            Dict with SHAP values and visualizations
        """
        logger.info("Computing SHAP values for Random Forest model")
        
        # Create explainer (use sample for speed)
        sample_size = min(100, X_test.shape[0])
        self.explainer = shap.TreeExplainer(model.model)
        
        # Calculate SHAP values
        self.shap_values = self.explainer.shap_values(X_test[:sample_size])
        
        # Get feature importance
        feature_importance = np.abs(self.shap_values).mean(axis=0)
        importance_dict = dict(zip(feature_names, feature_importance.tolist()))
        
        # Sort by importance
        sorted_importance = sorted(
            importance_dict.items(),
            key=lambda x: x[1],
            reverse=True
        )[:max_display]
        
        # Generate summary plot
        summary_plot = self._create_summary_plot(
            self.shap_values,
            X_test[:sample_size],
            feature_names,
            max_display
        )
        
        logger.info(f"SHAP analysis complete. Top feature: {sorted_importance[0][0]}")
        
        return {
            "feature_importance": dict(sorted_importance),
            "shap_values_shape": self.shap_values.shape,
            "summary_plot": summary_plot,
            "top_features": [f[0] for f in sorted_importance]
        }
    
    def explain_single_prediction(
        self,
        model,
        X_instance: np.ndarray,
        feature_names: List[str],
        model_type: str = "xgboost"
    ) -> Dict[str, Any]:
        """
        Explain a single prediction.
        
        Args:
            model: Trained model
            X_instance: Single instance features (1D or 2D)
            feature_names: List of feature names
            model_type: Type of model
        
        Returns:
            Dict with explanation
        """
        logger.info("Explaining single prediction")
        
        # Ensure 2D
        if X_instance.ndim == 1:
            X_instance = X_instance.reshape(1, -1)
        
        # Create explainer if not exists
        if self.explainer is None:
            if model_type in ["xgboost", "randomforest"]:
                self.explainer = shap.TreeExplainer(model.model)
            else:
                raise ValueError(f"Unsupported model type: {model_type}")
        
        # Calculate SHAP values
        shap_values = self.explainer.shap_values(X_instance)
        
        # Get feature contributions
        if shap_values.ndim > 1:
            shap_values = shap_values[0]
        
        contributions = dict(zip(feature_names, shap_values.tolist()))
        
        # Sort by absolute contribution
        sorted_contributions = sorted(
            contributions.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
        
        # Generate waterfall plot
        waterfall_plot = self._create_waterfall_plot(
            shap_values,
            X_instance[0],
            feature_names
        )
        
        return {
            "feature_contributions": dict(sorted_contributions[:10]),
            "base_value": float(self.explainer.expected_value),
            "prediction": float(model.predict(X_instance)[0]),
            "waterfall_plot": waterfall_plot
        }
    
    def _create_summary_plot(
        self,
        shap_values: np.ndarray,
        X: np.ndarray,
        feature_names: List[str],
        max_display: int = 10
    ) -> str:
        """Create SHAP summary plot and return as base64 string."""
        try:
            plt.figure(figsize=(10, 6))
            shap.summary_plot(
                shap_values,
                X,
                feature_names=feature_names,
                max_display=max_display,
                show=False
            )
            
            # Save to buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
            buf.seek(0)
            
            # Encode to base64
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()
            
            return f"data:image/png;base64,{img_base64}"
        
        except Exception as e:
            logger.error(f"Failed to create summary plot: {e}")
            return ""
    
    def _create_waterfall_plot(
        self,
        shap_values: np.ndarray,
        features: np.ndarray,
        feature_names: List[str]
    ) -> str:
        """Create SHAP waterfall plot and return as base64 string."""
        try:
            plt.figure(figsize=(10, 6))
            
            # Create explanation object
            explanation = shap.Explanation(
                values=shap_values,
                base_values=self.explainer.expected_value,
                data=features,
                feature_names=feature_names
            )
            
            shap.waterfall_plot(explanation, show=False)
            
            # Save to buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
            buf.seek(0)
            
            # Encode to base64
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()
            
            return f"data:image/png;base64,{img_base64}"
        
        except Exception as e:
            logger.error(f"Failed to create waterfall plot: {e}")
            return ""
    
    def get_feature_importance_native(
        self,
        model,
        feature_names: List[str],
        model_type: str = "xgboost"
    ) -> Dict[str, float]:
        """
        Get native feature importance from model.
        
        Args:
            model: Trained model
            feature_names: List of feature names
            model_type: Type of model
        
        Returns:
            Dict of feature importances
        """
        if model_type in ["xgboost", "randomforest"]:
            importance = model.model.feature_importances_
            return dict(zip(feature_names, importance.tolist()))
        else:
            raise ValueError(f"Native importance not available for {model_type}")
    
    def calculate_prediction_confidence(
        self,
        model,
        X: np.ndarray,
        n_iterations: int = 100,
        sample_fraction: float = 0.8
    ) -> Dict[str, Any]:
        """
        Calculate prediction confidence using bootstrap.
        
        Args:
            model: Trained model
            X: Input features
            n_iterations: Number of bootstrap iterations
            sample_fraction: Fraction of data to sample
        
        Returns:
            Dict with mean, std, and confidence intervals
        """
        logger.info(f"Calculating prediction confidence with {n_iterations} iterations")
        
        predictions = []
        n_samples = X.shape[0]
        sample_size = int(n_samples * sample_fraction)
        
        for _ in range(n_iterations):
            # Bootstrap sample
            indices = np.random.choice(n_samples, size=sample_size, replace=True)
            X_sample = X[indices]
            
            # Predict
            pred = model.predict(X_sample)
            predictions.append(pred.mean())
        
        predictions = np.array(predictions)
        
        return {
            "mean": float(predictions.mean()),
            "std": float(predictions.std()),
            "confidence_interval_95": {
                "lower": float(np.percentile(predictions, 2.5)),
                "upper": float(np.percentile(predictions, 97.5))
            },
            "confidence_interval_90": {
                "lower": float(np.percentile(predictions, 5)),
                "upper": float(np.percentile(predictions, 95))
            }
        }
