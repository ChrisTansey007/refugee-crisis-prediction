"""
Hyperparameter Tuning for LSTM Migration Forecasting Model
Implements automated hyperparameter optimization using Optuna
"""

import optuna
import torch
import torch.nn as nn
import numpy as np
from typing import Dict, Any, Tuple, List
import json
import os
from datetime import datetime

from app.models.ml_models import MLModel
from app.services.training_service import LSTMTrainingService
from app.data.processors import FeatureProcessor


class LSTMHyperparameterTuner:
    """
    Hyperparameter tuning for LSTM model using Optuna optimization.
    Optimizes for migration forecasting accuracy.
    """
    
    def __init__(self, study_name: str = "lstm_migration_forecasting"):
        self.study_name = study_name
        self.study = None
        self.best_params = None
        self.best_value = None
        
    def define_search_space(self, trial: optuna.Trial) -> Dict[str, Any]:
        """
        Define the hyperparameter search space for LSTM.
        
        Returns:
            Dictionary of hyperparameters to optimize
        """
        params = {
            # Architecture parameters
            'n_layers': trial.suggest_int('n_layers', 1, 3),
            'hidden_size': trial.suggest_categorical('hidden_size', [32, 64, 128, 256]),
            'dropout_rate': trial.suggest_float('dropout_rate', 0.1, 0.5),
            
            # Training parameters
            'learning_rate': trial.suggest_loguniform('learning_rate', 1e-4, 1e-2),
            'batch_size': trial.suggest_categorical('batch_size', [16, 32, 64, 128]),
            'sequence_length': trial.suggest_int('sequence_length', 6, 24),  # months
            
            # Regularization
            'weight_decay': trial.suggest_loguniform('weight_decay', 1e-6, 1e-3),
            'gradient_clip': trial.suggest_float('gradient_clip', 0.5, 2.0),
        }
        
        # Adjust hidden size based on number of layers
        if params['n_layers'] > 1:
            # Ensure hidden size is reasonable for deeper networks
            params['hidden_size'] = trial.suggest_categorical('hidden_size', [32, 64, 128])
            
        return params
    
    def create_lstm_model(self, input_size: int, params: Dict[str, Any]) -> nn.Module:
        """
        Create LSTM model with given hyperparameters.
        
        Args:
            input_size: Number of input features
            params: Hyperparameter dictionary
            
        Returns:
            Initialized LSTM model
        """
        class MigrationLSTM(nn.Module):
            def __init__(self, input_size, hidden_size, num_layers, dropout):
                super(MigrationLSTM, self).__init__()
                self.hidden_size = hidden_size
                self.num_layers = num_layers
                self.lstm = nn.LSTM(
                    input_size=input_size,
                    hidden_size=hidden_size,
                    num_layers=num_layers,
                    batch_first=True,
                    dropout=dropout if num_layers > 1 else 0
                )
                self.dropout = nn.Dropout(dropout)
                self.fc = nn.Linear(hidden_size, 1)  # Predicting refugee count
                
            def forward(self, x):
                # x shape: (batch, sequence_length, input_size)
                lstm_out, _ = self.lstm(x)
                # Take the last time step output
                last_output = lstm_out[:, -1, :]
                dropped = self.dropout(last_output)
                output = self.fc(dropped)
                return output.squeeze(-1)
        
        return MigrationLSTM(
            input_size=input_size,
            hidden_size=params['hidden_size'],
            num_layers=params['n_layers'],
            dropout=params['dropout_rate']
        )
    
    def objective(self, trial: optuna.Trial, X_train: np.ndarray, y_train: np.ndarray,
                  X_val: np.ndarray, y_val: np.ndarray) -> float:
        """
        Optuna objective function to minimize validation loss.
        
        Args:
            trial: Optuna trial object
            X_train, y_train: Training data
            X_val, y_val: Validation data
            
        Returns:
            Validation RMSE (to be minimized)
        """
        try:
            # Get hyperparameters for this trial
            params = self.define_search_space(trial)
            
            # Create model
            input_size = X_train.shape[2] if len(X_train.shape) == 3 else X_train.shape[1]
            model = self.create_lstm_model(input_size, params)
            
            # Create training service
            trainer = LSTMTrainingService(
                model=model,
                learning_rate=params['learning_rate'],
                batch_size=params['batch_size'],
                weight_decay=params['weight_decay'],
                gradient_clip=params['gradient_clip']
            )
            
            # Train model
            train_losses, val_losses = trainer.train(
                X_train, y_train,
                X_val, y_val,
                epochs=50,  # Reduced for tuning
                verbose=False
            )
            
            # Return best validation loss
            best_val_loss = min(val_losses) if val_losses else float('inf')
            
            # Report intermediate values for pruning
            trial.report(best_val_loss, len(val_losses)-1)
            
            # Handle pruning
            if trial.should_prune():
                raise optuna.TrialPruned()
                
            return best_val_loss
            
        except Exception as e:
            print(f"Trial failed with error: {e}")
            return float('inf')  # Return worst possible score
    
    def optimize(self, X_train: np.ndarray, y_train: np.ndarray,
                 X_val: np.ndarray, y_val: np.ndarray,
                 n_trials: int = 50) -> Dict[str, Any]:
        """
        Run hyperparameter optimization.
        
        Args:
            X_train, y_train: Training data
            X_val, y_val: Validation data
            n_trials: Number of optimization trials
            
        Returns:
            Best hyperparameters found
        """
        # Create study
        sampler = optuna.samplers.TPESampler(seed=42)
        pruner = optuna.pruners.MedianPruner()
        self.study = optuna.create_study(
            direction='minimize',
            sampler=sampler,
            pruner=pruner,
            study_name=self.study_name
        )
        
        # Optimize
        self.study.optimize(
            lambda trial: self.objective(trial, X_train, y_train, X_val, y_val),
            n_trials=n_trials,
            timeout=None  # No timeout
        )
        
        # Store best results
        self.best_params = self.study.best_params
        self.best_value = self.study.best_value
        
        print(f"Optimization completed!")
        print(f"Best validation RMSE: {self.best_value:.4f}")
        print(f"Best hyperparameters: {json.dumps(self.best_params, indent=2)}")
        
        return self.best_params
    
    def save_study_results(self, filepath: str):
        """Save study results to JSON file."""
        results = {
            'study_name': self.study_name,
            'best_value': self.best_value,
            'best_params': self.best_params,
            'n_trials': len(self.study.trials),
            'completed_trials': len([t for t in self.study.trials if t.state == optuna.trial.TrialState.COMPLETE]),
            'pruned_trials': len([t for t in self.study.trials if t.state == optuna.trial.TrialState.PRUNED]),
            'failed_trials': len([t for t in self.study.trials if t.state == optuna.trial.TrialState.FAIL]),
            'timestamp': datetime.now().isoformat()
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Study results saved to {filepath}")
    
    def get_optimization_history(self) -> List[Dict]:
        """Get optimization history for analysis."""
        if self.study is None:
            return []
            
        history = []
        for trial in self.study.trials:
            if trial.state == optuna.trial.TrialState.COMPLETE:
                history.append({
                    'trial_number': trial.number,
                    'value': trial.value,
                    'params': trial.params,
                    'state': str(trial.state)
                })
        return history


# Example usage function
def run_hyperparameter_tuning_example():
    """
    Example of how to use the LSTMHyperparameterTuner.
    In practice, this would be called with real training data.
    """
    print("LSTM Hyperparameter Tuner initialized")
    print("To use:")
    print("1. Prepare training data (X_train, y_train, X_val, y_val)")
    print("2. Create tuner: tuner = LSTMHyperparameterTuner()")
    print("3. Run optimization: best_params = tuner.optimize(X_train, y_train, X_val, y_val)")
    print("4. Save results: tuner.save_study_results('path/to/results.json')")
    
    # Return tuner for use
    return LSTMHyperparameterTuner()


if __name__ == "__main__":
    # Example usage
    tuner = run_hyperparameter_tuning_example()
    print("
Hyperparameter tuner ready for use with real data.")
