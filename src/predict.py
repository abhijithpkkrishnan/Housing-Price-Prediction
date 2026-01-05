"""
Prediction module for housing price prediction
"""

import pickle
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score


def make_predictions(model, X_test, y_test, output_path='outputs/actual_vs_predicted.png'):
    """
    Make predictions and visualize results
    
    Args:
        model: Trained model object
        X_test (DataFrame): Test features
        y_test (Series): Test target values
        output_path (str): Path to save the visualization
    
    Returns:
        array: Predicted values
    """
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nPrediction Metrics:")
    print(f"RMSE: {rmse:.4f}")
    print(f"R² Score: {r2:.4f}")
    
    # Create visualization
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Prices')
    plt.ylabel('Predicted Prices')
    plt.title('Actual vs Predicted House Prices')
    plt.grid(True, alpha=0.3)
    
    # Save the plot
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Visualization saved to {output_path}")
    plt.close()
    
    return y_pred


def predict_single(model, features):
    """
    Make prediction for a single sample
    
    Args:
        model: Trained model object
        features (array or DataFrame): Input features
    
    Returns:
        float: Predicted price
    """
    prediction = model.predict([features] if isinstance(features, (list, np.ndarray)) and len(np.array(features).shape) == 1 else features)
    return prediction[0]


def load_and_predict(model_path, X_test, y_test=None):
    """
    Load model and make predictions
    
    Args:
        model_path (str): Path to the saved model
        X_test (DataFrame): Test features
        y_test (Series): Test target values (optional)
    
    Returns:
        array: Predicted values
    """
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    predictions = model.predict(X_test)
    
    if y_test is not None:
        r2 = r2_score(y_test, predictions)
        print(f"R² Score: {r2:.4f}")
    
    return predictions
