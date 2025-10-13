from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, Text, JSON, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class MLModel(Base):
    """Table for storing trained ML models metadata."""
    
    __tablename__ = "ml_models"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    model_type: Mapped[str] = mapped_column(String(50), nullable=False)  # LSTM, XGBoost, RandomForest
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    country_iso: Mapped[str] = mapped_column(String(3), nullable=True)
    target_variable: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Training metadata
    training_start_date: Mapped[str] = mapped_column(String(10), nullable=True)
    training_end_date: Mapped[str] = mapped_column(String(10), nullable=True)
    n_features: Mapped[int] = mapped_column(Integer, nullable=True)
    feature_list: Mapped[dict] = mapped_column(JSON, nullable=True)
    
    # Hyperparameters
    hyperparameters: Mapped[dict] = mapped_column(JSON, nullable=True)
    
    # Performance metrics
    test_rmse: Mapped[float] = mapped_column(Float, nullable=True)
    test_mae: Mapped[float] = mapped_column(Float, nullable=True)
    test_r2: Mapped[float] = mapped_column(Float, nullable=True)
    
    # MLflow tracking
    mlflow_run_id: Mapped[str] = mapped_column(String(255), nullable=True)
    mlflow_experiment_id: Mapped[str] = mapped_column(String(255), nullable=True)
    
    # Model artifacts
    model_path: Mapped[str] = mapped_column(String(500), nullable=True)
    scaler_path: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(50), default="trained", nullable=False)  # trained, deployed, archived
    is_active: Mapped[bool] = mapped_column(default=False, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Notes
    notes: Mapped[str] = mapped_column(Text, nullable=True)


class Prediction(Base):
    """Table for storing model predictions."""
    
    __tablename__ = "predictions"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    model_id: Mapped[int] = mapped_column(Integer, nullable=False)
    country_iso: Mapped[str] = mapped_column(String(3), nullable=False)
    prediction_date: Mapped[str] = mapped_column(String(10), nullable=False)  # Date being predicted
    predicted_value: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_lower: Mapped[float] = mapped_column(Float, nullable=True)
    confidence_upper: Mapped[float] = mapped_column(Float, nullable=True)
    actual_value: Mapped[float] = mapped_column(Float, nullable=True)  # Filled in later for evaluation
    
    # Input features (for explainability)
    input_features: Mapped[dict] = mapped_column(JSON, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
