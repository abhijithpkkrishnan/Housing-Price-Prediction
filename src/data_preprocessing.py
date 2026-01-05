"""
Data preprocessing module for housing price prediction
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def preprocess_data(file_path, test_size=0.2, random_state=42):
    """
    Load and preprocess housing data
    
    Args:
        file_path (str): Path to the CSV file
        test_size (float): Proportion of test set
        random_state (int): Random seed for reproducibility
    
    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    
    # Load data
    df = pd.read_csv(file_path)
    
    # Remove missing values
    df = df.dropna()
    
    # Separate features and target
    X = df.drop('price', axis=1)
    y = df['price']
    
    # Encode categorical variables
    X = encode_categorical(X)
    
    # Save columns
    os.makedirs('models', exist_ok=True)
    with open('models/model_columns.pkl', 'wb') as f:
        pickle.dump(X.columns, f)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save scaler
    with open('models/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

    # Convert back to DataFrame to maintain column names
    X_train = pd.DataFrame(X_train_scaled, columns=X.columns)
    X_test = pd.DataFrame(X_test_scaled, columns=X.columns)
    
    print(f"Data shape: {df.shape}")
    print(f"Training set: {X_train.shape}")
    print(f"Test set: {X_test.shape}")
    
    return X_train, X_test, y_train, y_test


def handle_missing_values(df, strategy='mean'):
    """
    Handle missing values in the dataset
    
    Args:
        df (DataFrame): Input dataframe
        strategy (str): Strategy to handle missing values
    
    Returns:
        DataFrame: Dataframe with handled missing values
    """
    if strategy == 'mean':
        return df.fillna(df.mean())
    elif strategy == 'median':
        return df.fillna(df.median())
    else:
        return df.dropna()


def encode_categorical(df):
    """
    Encode categorical variables
    
    Args:
        df (DataFrame): Input dataframe
    
    Returns:
        DataFrame: Dataframe with encoded categorical variables
    """
    return pd.get_dummies(df, drop_first=True)
