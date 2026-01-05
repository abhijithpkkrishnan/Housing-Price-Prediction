"""
Model training module for housing price prediction
"""

import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error


def train_model(X_train, y_train, model_type='linear', save_path='models/house_price_model.pkl'):
    """
    Train a machine learning model
    
    Args:
        X_train (DataFrame): Training features
        y_train (Series): Training target
        model_type (str): Type of model ('linear' or 'random_forest')
        save_path (str): Path to save the trained model
    
    Returns:
        model: Trained model object
    """
    
    if model_type == 'linear':
        model = LinearRegression()
    elif model_type == 'random_forest':
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Save the model
    with open(save_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Model trained and saved to {save_path}")
    
    return model


def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance
    
    Args:
        model: Trained model object
        X_test (DataFrame): Test features
        y_test (Series): Test target
    
    Returns:
        dict: Dictionary with evaluation metrics
    """
    
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    metrics = {
        'MSE': mse,
        'RMSE': rmse,
        'MAE': mae,
        'R2 Score': r2
    }
    
    print("\nModel Evaluation Metrics:")
    print("-" * 30)
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")
    
    return metrics


def load_model(model_path):
    """
    Load a trained model from disk
    
    Args:
        model_path (str): Path to the saved model
    
    Returns:
        model: Loaded model object
    """
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model
