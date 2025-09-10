# File Name: ml_manager.py
# This module contains all the backend logic for the interactive classification lab.

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib
import json
import os
from datetime import datetime

# --- Constants ---
HISTORY_FILE = "training_history.json"

# ------------------------------------------------------------------
# 1. DATA HANDLING FUNCTIONS
# ------------------------------------------------------------------
def load_data(uploaded_file):
    """Loads data from an uploaded CSV file."""
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        return f"Error loading CSV file: {e}"

def get_data_info(df):
    """Returns basic information about the dataframe."""
    return {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "missing_values": df.isnull().sum(),
        "numerical_cols": df.select_dtypes(include=np.number).columns.tolist(),
        "categorical_cols": df.select_dtypes(include=['object', 'category']).columns.tolist()
    }

def clean_data(df, columns_to_drop, missing_value_strategies):
    """
    Cleans the data based on user-defined strategies.
    """
    df_cleaned = df.copy()
    
    df_cleaned.drop(columns=columns_to_drop, errors='ignore', inplace=True)

    for col, strategy in missing_value_strategies.items():
        if col in df_cleaned.columns:
            if strategy == 'Drop Rows':
                df_cleaned.dropna(subset=[col], inplace=True)
            elif strategy == 'Fill with Mean':
                if pd.api.types.is_numeric_dtype(df_cleaned[col]):
                    df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mean())
            elif strategy == 'Fill with Median':
                if pd.api.types.is_numeric_dtype(df_cleaned[col]):
                    df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())
            elif strategy == 'Fill with Mode':
                df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mode()[0])
    
    label_encoders = {}
    for col in df_cleaned.select_dtypes(include=['object', 'category']).columns:
        le = LabelEncoder()
        df_cleaned[col] = le.fit_transform(df_cleaned[col].astype(str))
        label_encoders[col] = le
        
    return df_cleaned, label_encoders

# ------------------------------------------------------------------
# 2. MODEL TRAINING AND EVALUATION
# ------------------------------------------------------------------
def train_classification_model(df, target_column, model_name, test_size=0.2):
    """
    Trains a selected classification model and returns its performance.
    """
    if target_column not in df.columns:
        return None, "Error: Target column not found in the cleaned data.", None, None

    X = df.drop(target_column, axis=1)
    y = df[target_column]

    # --- ERROR FIX ---
    # Check if stratification is possible. It requires at least 2 members per class.
    stratify_param = None
    if y.nunique() > 1 and y.value_counts().min() >= 2:
        stratify_param = y

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42, stratify=stratify_param)

    if model_name == "Logistic Regression":
        model = LogisticRegression(max_iter=1000)
    elif model_name == "Random Forest":
        model = RandomForestClassifier(n_estimators=100, random_state=42)
    elif model_name == "Support Vector Machine (SVM)":
        model = SVC(probability=True, random_state=42)
    else:
        return None, "Error: Invalid model name selected.", None, None

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    joblib.dump(model, 'trained_classifier.pkl')
    
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    class_report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    
    # Get class labels for the confusion matrix
    class_labels = sorted(y.unique())

    save_training_history({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dataset_shape": list(df.shape),
        "model_name": model_name,
        "target_column": target_column,
        "accuracy": accuracy,
        "test_size": test_size
    })

    return model, {"accuracy": accuracy, "conf_matrix": conf_matrix, "class_report": class_report, "labels": class_labels}, X.columns.tolist()

# ------------------------------------------------------------------
# 3. HISTORY AND PREDICTION
# ------------------------------------------------------------------
def save_training_history(log_entry):
    """Saves a log of the training session to a JSON file."""
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            try: history = json.load(f)
            except json.JSONDecodeError: history = []
    history.append(log_entry)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def load_training_history():
    """Loads the training history from the JSON file."""
    if not os.path.exists(HISTORY_FILE): return []
    with open(HISTORY_FILE, 'r') as f:
        try: return json.load(f)
        except json.JSONDecodeError: return []

def make_prediction(model, features, input_data, label_encoders, original_df, target_column):
    """Makes a prediction on new, user-provided data."""
    input_df = pd.DataFrame([input_data])
    
    for col, le in label_encoders.items():
        if col in input_df.columns:
            known_classes = list(le.classes_)
            input_df[col] = input_df[col].apply(lambda x: le.transform([x])[0] if x in known_classes else -1)

    input_df = input_df.reindex(columns=features, fill_value=0)
    
    prediction = model.predict(input_df)
    prediction_proba = model.predict_proba(input_df)
    
    # Inverse transform the prediction to its original label
    if target_column in label_encoders:
        prediction_label = label_encoders[target_column].inverse_transform(prediction)[0]
    else:
        prediction_label = prediction[0]

    return prediction_label, prediction_proba[0]
