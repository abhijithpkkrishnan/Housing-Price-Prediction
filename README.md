# Housing Price Prediction

A machine learning project to predict house prices based on various features.

## Project Structure

```
Housing-Price-Prediction/
│
├── data/
│   └── housing.csv
│
├── notebooks/
│   └── EDA.ipynb
│
├── src/
│   ├── data_preprocessing.py
│   ├── train_model.py
│   └── predict.py
│
├── models/
│   └── house_price_model.pkl
│
├── outputs/
│   └── actual_vs_predicted.png
│
├── requirements.txt
├── README.md
└── main.py
```

## Getting Started

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Place your housing data in the `data/` folder as `housing.csv`

3. Run the main script:
   ```bash
   python main.py
   ```

## Project Components

- **data_preprocessing.py**: Handles data cleaning and feature engineering
- **train_model.py**: Trains the machine learning model
- **predict.py**: Makes predictions on new data
- **EDA.ipynb**: Exploratory Data Analysis notebook
- **main.py**: Main entry point of the project

## Files Generated

- **house_price_model.pkl**: Trained model saved in the models folder
- **actual_vs_predicted.png**: Visualization of predictions in the outputs folder
