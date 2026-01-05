import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
from PIL import Image

def load_artifacts():
    try:
        with open('models/house_price_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('models/scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        with open('models/model_columns.pkl', 'rb') as f:
            model_columns = pickle.load(f)
        return model, scaler, model_columns
    except FileNotFoundError:
        st.error("Model artifacts not found. Please run 'python main.py' first.")
        return None, None, None

def main():
    st.set_page_config(page_title="Housing Price Prediction", page_icon="🏠")
    
    # Custom CSS for Dark Neumorphic Design
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

        /* Global Styles */
        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif;
        }

        /* Background color */
        .stApp {
            background-color: #141b2d;
            color: #ffffff;
        }
        
        /* Neumorphic container */
        .css-1r6slb0, .css-12oz5g7 {
            border-radius: 20px;
            background: #141b2d;
            box-shadow:  20px 20px 60px #0b0f19,
                        -20px -20px 60px #1d2741;
            padding: 20px;
        }

        /* Inputs */
        .stTextInput > div > div > input, 
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > div {
            border-radius: 10px;
            background: #141b2d;
            box-shadow: inset 5px 5px 10px #0b0f19,
                        inset -5px -5px 10px #1d2741;
            border: none;
            color: #ffffff;
        }
        
        /* Selectbox Dropdown specific fix */
        .stSelectbox > div > div > div:hover {
             color: #ffffff;
        }

        /* Labels */
        .stNumberInput label, .stSelectbox label {
            color: #e0e5ec !important;
            font-weight: 500;
        }

        /* Buttons */
        .stButton > button {
            border-radius: 50px;
            background: #141b2d;
            box-shadow:  5px 5px 10px #0b0f19,
                        -5px -5px 10px #1d2741;
            border: none;
            color: #ffffff;
            font-weight: bold;
            transition: all 0.2s ease-in-out;
            letter-spacing: 1px;
        }

        .stButton > button:hover {
            box-shadow: inset 5px 5px 10px #0b0f19,
                        inset -5px -5px 10px #1d2741;
            color: #64b5f6;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #ffffff !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            font-weight: 600;
        }
        
        /* Normal text */
        p, span {
            color: #e0e5ec;
        }
        
        /* Success message */
        .stSuccess {
            background-color: #141b2d;
            color: #4caf50;
            border: none;
            box-shadow: inset 3px 3px 6px #0b0f19,
                        inset -3px -3px 6px #1d2741;
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🏠 Housing Price Prediction")
    st.write("Enter the details of the house to estimate its price.")
    
    model, scaler, model_columns = load_artifacts()
    
    if model is None:
        return

    # Create input form
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            area = st.number_input("Area (sq ft)", min_value=100, value=5000)
            bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=3)
            bathrooms = st.number_input("Bathrooms", min_value=1, max_value=5, value=1)
            stories = st.number_input("Stories", min_value=1, max_value=5, value=1)
            parking = st.number_input("Parking Spots", min_value=0, max_value=5, value=0)
            
        with col2:
            mainroad = st.selectbox("Main Road Access", ["yes", "no"])
            guestroom = st.selectbox("Guestroom", ["yes", "no"])
            basement = st.selectbox("Basement", ["yes", "no"])
            hotwaterheating = st.selectbox("Hot Water Heating", ["yes", "no"])
            airconditioning = st.selectbox("Air Conditioning", ["yes", "no"])
            prefarea = st.selectbox("Preferred Area", ["yes", "no"])
            furnishingstatus = st.selectbox("Furnishing Status", ["furnished", "semi-furnished", "unfurnished"])
            
        submit_button = st.form_submit_button("Predict Price")
        
    if submit_button:
        # Create dataframe from input
        input_data = pd.DataFrame({
            'area': [area],
            'bedrooms': [bedrooms],
            'bathrooms': [bathrooms],
            'stories': [stories],
            'mainroad': [mainroad],
            'guestroom': [guestroom],
            'basement': [basement],
            'hotwaterheating': [hotwaterheating],
            'airconditioning': [airconditioning],
            'parking': [parking],
            'prefarea': [prefarea],
            'furnishingstatus': [furnishingstatus]
        })
        
        # Preprocess input
        # 1. Encode categorical variables
        input_encoded = pd.get_dummies(input_data, drop_first=True)
        
        # 2. Align columns with training data
        # Get missing columns in the training test
        missing_cols = set(model_columns) - set(input_encoded.columns)
        # Add a missing column in test set with default value equal to 0
        for c in missing_cols:
            input_encoded[c] = 0
            
        # Ensure the order of column in the test set is in the same order than in train set
        input_encoded = input_encoded[model_columns]
        
        # 3. Scale features
        input_scaled = scaler.transform(input_encoded)
        
        # 4. Predict
        prediction = model.predict(input_scaled)
        
        st.success(f"Estimated Price: ${prediction[0]:,.2f}")
        
    st.markdown("---")
    st.subheader("Model Performance Visualization")
    try:
        image = Image.open('outputs/actual_vs_predicted.png')
        st.image(image, caption='Actual vs Predicted House Prices', use_container_width=True)
    except FileNotFoundError:
        st.warning("Visualization not found. Run the training pipeline to generate it.")

if __name__ == "__main__":
    main()
