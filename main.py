"""
Main entry point for the Housing Price Prediction project
"""

import sys
from src.data_preprocessing import preprocess_data
from src.train_model import train_model
from src.predict import make_predictions


def main():
    """
    Main function to orchestrate the entire pipeline
    """
    print("=" * 50)
    print("Housing Price Prediction Project")
    print("=" * 50)
    
    try:
        # Step 1: Data Preprocessing
        print("\n[1/3] Loading and preprocessing data...")
        X_train, X_test, y_train, y_test = preprocess_data('data/housing.csv')
        print("✓ Data preprocessing completed")
        
        # Step 2: Train Model
        print("\n[2/3] Training the model...")
        model = train_model(X_train, y_train)
        print("✓ Model training completed")
        
        # Step 3: Make Predictions
        print("\n[3/3] Making predictions...")
        make_predictions(model, X_test, y_test)
        print("✓ Predictions completed")
        
        print("\n" + "=" * 50)
        print("Pipeline execution completed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n✗ Error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
