"""
Training Service for LSTM Model
Handles model training, validation, and checkpointing
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Tuple, List, Optional
import logging

logger = logging.getLogger(__name__)


class LSTMTrainingService:
    """
    Service for training LSTM models for migration forecasting.
    """
    
    def __init__(self, model: nn.Module, learning_rate: float = 0.001,
                 batch_size: int = 32, weight_decay: float = 1e-5,
                 gradient_clip: float = 1.0):
        """
        Initialize training service.
        
        Args:
            model: PyTorch model to train
            learning_rate: Learning rate for optimizer
            batch_size: Batch size for training
            weight_decay: L2 regularization strength
            gradient_clip: Gradient clipping threshold
        """
        self.model = model
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.weight_decay = weight_decay
        self.gradient_clip = gradient_clip
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Move model to device
        self.model.to(self.device)
        
        # Initialize optimizer and loss function
        self.optimizer = torch.optim.Adam(
            self.model.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay
        )
        self.criterion = nn.MSELoss()
        
        logger.info(f"LSTMTrainingService initialized on {self.device}")
    
    def prepare_data(self, X: np.ndarray, y: np.ndarray) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Convert numpy arrays to PyTorch tensors and move to device.
        
        Args:
            X: Input features array
            y: Target values array
            
        Returns:
            Tuple of (X_tensor, y_tensor) on device
        """
        X_tensor = torch.FloatTensor(X).to(self.device)
        y_tensor = torch.FloatTensor(y).to(self.device)
        return X_tensor, y_tensor
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray,
              X_val: np.ndarray, y_val: np.ndarray,
              epochs: int = 100, verbose: bool = True) -> Tuple[List[float], List[float]]:
        """
        Train the LSTM model.
        
        Args:
            X_train, y_train: Training data
            X_val, y_val: Validation data
            epochs: Number of training epochs
            verbose: Whether to print training progress
            
        Returns:
            Tuple of (train_losses, val_losses) lists
        """
        # Prepare data
        X_train_tensor, y_train_tensor = self.prepare_data(X_train, y_train)
        X_val_tensor, y_val_tensor = self.prepare_data(X_val, y_val)
        
        train_losses = []
        val_losses = []
        
        self.model.train()
        
        for epoch in range(epochs):
            # Training phase
            epoch_train_loss = 0.0
            n_batches = 0
            
            # Mini-batch training
            for i in range(0, len(X_train_tensor), self.batch_size):
                batch_X = X_train_tensor[i:i+self.batch_size]
                batch_y = y_train_tensor[i:i+self.batch_size]
                
                # Forward pass
                self.optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = self.criterion(outputs, batch_y)
                
                # Backward pass
                loss.backward()
                
                # Gradient clipping
                if self.gradient_clip > 0:
                    torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.gradient_clip)
                
                self.optimizer.step()
                
                epoch_train_loss += loss.item()
                n_batches += 1
            
            avg_train_loss = epoch_train_loss / max(n_batches, 1)
            train_losses.append(avg_train_loss)
            
            # Validation phase
            self.model.eval()
            with torch.no_grad():
                val_outputs = self.model(X_val_tensor)
                val_loss = self.criterion(val_outputs, y_val_tensor)
                val_losses.append(val_loss.item())
            
            self.model.train()  # Back to training mode
            
            # Print progress
            if verbose and (epoch + 1) % 10 == 0:
                logger.info(
                    f'Epoch [{epoch+1}/{epochs}], '
                    f'Train Loss: {avg_train_loss:.4f}, '
                    f'Val Loss: {val_loss.item():.4f}'
                )
        
        logger.info(f'Training completed. Final train loss: {train_losses[-1]:.4f}, '
                   f'Final val loss: {val_losses[-1]:.4f}')
        
        return train_losses, val_losses
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions using the trained model.
        
        Args:
            X: Input features array
            
        Returns:
            Predictions as numpy array
        """
        self.model.eval()
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X).to(self.device)
            predictions = self.model(X_tensor)
            return predictions.cpu().numpy()
    
    def save_model(self, filepath: str, metadata: Optional[dict] = None):
        """
        Save model checkpoint.
        
        Args:
            filepath: Path to save model
            metadata: Optional metadata to save with model
        """
        checkpoint = {
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'model_architecture': str(self.model),
            'hyperparameters': {
                'learning_rate': self.learning_rate,
                'batch_size': self.batch_size,
                'weight_decay': self.weight_decay,
                'gradient_clip': self.gradient_clip
            },
            'metadata': metadata or {}
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        torch.save(checkpoint, filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """
        Load model checkpoint.
        
        Args:
            filepath: Path to load model from
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
            
        checkpoint = torch.load(filepath, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        logger.info(f"Model loaded from {filepath}")
        
        return checkpoint.get('metadata', {})
