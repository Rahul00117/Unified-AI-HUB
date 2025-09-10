# File Name: regression_manager.py
# This module contains all the backend logic for the regression model.

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import io

def get_default_data():
    """
    Provides a default dataset if none is uploaded.
    Returns a pandas DataFrame.
    """
    data = {
        'Hours': [2.5, 5.1, 3.2, 8.5, 3.5, 1.5, 9.2, 5.5, 8.3, 2.7, 7.7, 5.9, 4.5, 3.3, 1.1, 8.9, 2.5, 1.9, 6.1, 7.4, 2.7, 4.8, 3.8, 6.9, 7.8],
        'Scores': [21, 47, 27, 75, 30, 20, 88, 60, 81, 25, 85, 62, 41, 42, 17, 95, 30, 24, 67, 69, 30, 54, 35, 76, 86]
    }
    return pd.DataFrame(data)

def load_and_clean_data(uploaded_file):
    """
    Loads data from an uploaded CSV file and cleans it.
    Returns a pandas DataFrame or None if an error occurs.
    """
    try:
        df = pd.read_csv(uploaded_file)
        # Ensure there are at least two columns
        if df.shape[1] < 2:
            return "Error: The CSV file must have at least two columns (for Hours and Marks)."
        
        # Use the first two columns and rename them for consistency
        df = df.iloc[:, :2]
        df.columns = ['Hours', 'Scores']
        
        # Convert to numeric, coercing errors to NaN (Not a Number)
        df = df.apply(pd.to_numeric, errors='coerce')
        # Drop any rows that have missing values after conversion
        df.dropna(inplace=True)
        
        return df
    except Exception as e:
        return f"Error processing file: {e}"

def train_regression_model(df):
    """
    Trains a Linear Regression model on the provided DataFrame.
    Returns the trained model, feature data (X), and target data (y).
    """
    if df.empty:
        return None, None, None
        
    # Prepare data for the model
    X = df[['Hours']] # Features should be a DataFrame
    y = df['Scores']  # Target can be a Series

    # Initialize and train the model
    model = LinearRegression()
    model.fit(X, y)
    
    return model, X, y

def get_model_performance(model, X, y):
    """
    Calculates performance metrics for the trained model.
    Returns the R-squared score and the regression equation as a string.
    """
    # Make predictions on the training data to calculate R-squared
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    
    # Get the model's coefficient (slope) and intercept
    slope = model.coef_[0]
    intercept = model.intercept_
    
    equation = f"Marks = {slope:.2f} × Hours + {intercept:.2f}"
    
    return r2, equation

def predict_marks(model, hours):
    """
    Makes a prediction for a given number of hours.
    Returns the predicted marks.
    """

    # The model expects a 2D array, so we reshape the input
    hours_reshaped = np.array([[hours]])
    prediction = model.predict(hours_reshaped)
    return prediction[0]
