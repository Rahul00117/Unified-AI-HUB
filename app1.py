# program-1
# File Name: app.py
# This is the main application file that runs the Streamlit UI.

import streamlit as st
import vehicle_manager # Import your custom backend module

# --- Configuration ---
# IMPORTANT: Replace "YOUR_GEMINI_API_KEY_HERE" with your actual Gemini API key
GEMINI_API_KEY = "AIzaSyDD3oJrnnH_V8EgVDfThay8X1iTCTvrHgA"

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="AI Vehicle Hub", layout="wide", page_icon="🚗")

# --- Sidebar ---
st.sidebar.header("⚙️ Configuration")
if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
    st.sidebar.warning("API Key not set! Please edit the code.")
else:
    st.sidebar.success("API Key is configured.")

# --- Main App UI ---
st.title("🚗 AI Vehicle Recommender Hub")
st.info("Your personal AI assistant to find the perfect vehicle. Fill in your preferences and get instant recommendations with images!")

# Create tabs for different vehicle types
tab1, tab2, tab3 = st.tabs(["🏍️ 2-Wheeler Recommender", "🚙 4-Wheeler Recommender", "🧠 Ask Anything"])

# --- Helper function to display results ---
def display_results(results):
    if isinstance(results, list):
        for item in results:
            data = item.get("data", {})
            image_url = item.get("image_url")
            
            with st.container():
                col_img, col_text = st.columns([1, 2])
                with col_img:
                    st.image(image_url, caption=data.get("model_name", "Vehicle Image"), use_container_width=True)
                with col_text:
                    st.subheader(f"**{data.get('model_name', 'N/A')}**")
                    st.write(f"**Brand:** {data.get('brand', 'N/A')}")
                    st.write(f"**Price (INR):** ₹{data.get('price_inr', 'N/A')}")
                    st.write(f"**Fuel:** {data.get('fuel_type', 'N/A')}")
                    if data.get('transmission', 'N/A') != 'N/A':
                        st.write(f"**Transmission:** {data.get('transmission')}")
                    if data.get('seating', 'N/A') != 'N/A':
                        st.write(f"**Seating:** {data.get('seating')}")
                    st.write(f"**Reason:** {data.get('reason', 'N/A')}")
                st.markdown("---")
    else: # Display error message if it's a string
        st.error(results)

# --- Tab 1: 2-Wheeler Recommender ---
with tab1:
    st.subheader("Find Your Perfect 2-Wheeler")
    with st.form("form_2wheeler"):
        # UI elements... (same as before)
        col1, col2 = st.columns(2)
        with col1:
            fuel_2w = st.radio("Fuel Type", ["Petrol", "Electric"], key="fuel_2w")
            brand_2w = st.selectbox("Brand", ["Any", "Hero", "TVS", "Honda", "Bajaj", "Royal Enfield", "Yamaha", "Ola Electric"], key="brand_2w")
        with col2:
            budget_2w = st.slider("Maximum Budget (₹)", 20000, 300000, step=5000, value=80000, key="budget_2w")
            usage_2w = st.selectbox("Primary Usage", ["Daily Commute", "Touring / Long Rides", "Sport / Performance", "Off-road"], key="usage_2w")
        look_2w = st.text_input("Desired Look & Style", placeholder="e.g., Sporty, Retro, Cruiser", key="look_2w")
        extra_2w = st.text_area("Any other preferences?", placeholder="e.g., good mileage, comfortable seat", key="extra_2w")
        
        submitted_2w = st.form_submit_button("🔍 Get 2-Wheeler Suggestions", use_container_width=True)
        
        if submitted_2w:
            if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
                st.error("Please set your Gemini API Key in the app.py file.")
            else:
                with st.spinner("🏍️ Finding the best bikes for you..."):
                    results = vehicle_manager.recommend_2wheeler(GEMINI_API_KEY, fuel_2w, budget_2w, brand_2w, usage_2w, look_2w, extra_2w)
                    display_results(results)

# --- Tab 2: 4-Wheeler Recommender ---
with tab2:
    st.subheader("Find Your Perfect 4-Wheeler")
    with st.form("form_4wheeler"):
        # UI elements... (same as before)
        col1, col2 = st.columns(2)
        with col1:
            fuel_4w = st.radio("Fuel Type", ["Petrol", "Diesel", "Electric", "CNG", "Hybrid"], key="fuel_4w")
            brand_4w = st.selectbox("Brand", ["Any", "Tata", "Maruti Suzuki", "Hyundai", "Mahindra", "Kia", "Toyota"], key="brand_4w")
            usage_4w = st.selectbox("Primary Usage", ["City Driving", "Family Car", "Long Highway Drives", "Off-road"], key="usage_4w")
        with col2:
            budget_4w = st.slider("Maximum Budget (₹)", 300000, 5000000, step=25000, value=1000000, key="budget_4w")
            seating_4w = st.slider("Minimum Seating Capacity", 4, 9, 5, key="seating_4w")
            transmission_4w = st.radio("Transmission", ["Manual", "Automatic", "Any"], key="transmission_4w")
        look_4w = st.text_input("Desired Look & Style", placeholder="e.g., SUV, Sedan, Hatchback", key="look_4w")
        extra_4w = st.text_area("Any other preferences?", placeholder="e.g., high safety rating, sunroof", key="extra_4w")

        submitted_4w = st.form_submit_button("🚙 Get 4-Wheeler Suggestions", use_container_width=True)

        if submitted_4w:
            if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
                st.error("Please set your Gemini API Key in the app.py file.")
            else:
                with st.spinner("🚗 Searching for the best cars for you..."):
                    results = vehicle_manager.recommend_4wheeler(GEMINI_API_KEY, fuel_4w, budget_4w, brand_4w, seating_4w, usage_4w, transmission_4w, look_4w, extra_4w)
                    display_results(results)

# --- Tab 3: Ask Anything ---
with tab3:
    st.subheader("Ask a Custom Question")
    custom_prompt = st.text_area("Your Question:", placeholder="e.g., 'Compare Tata Nexon EV and Mahindra XUV400'", height=150)
    
    if st.button("🧠 Ask Gemini"):
        if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            st.error("Please set your Gemini API Key in the app.py file.")
        elif not custom_prompt:
            st.warning("Please enter a question.")
        else:
            with st.spinner("🤖 Gemini is thinking..."):
                results = vehicle_manager.ask_anything(GEMINI_API_KEY, custom_prompt)
                display_results(results)











# program-2
# File Name: app.py
# This is the main application file that runs the Streamlit UI.

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Import your custom backend module
import regression_manager

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Study Hours vs Marks Predictor", layout="wide", page_icon="📚")

# --- Main App UI ---
st.title("📚 Study Hours vs Marks Predictor")
st.write("An interactive web app to visualize and predict student marks based on study hours using Linear Regression.")

# --- Sidebar for Data Input ---
st.sidebar.header("Data Configuration")
uploaded_file = st.sidebar.file_uploader("Upload your own CSV file", type=["csv"])

# Load data based on user choice
if uploaded_file is not None:
    data = regression_manager.load_and_clean_data(uploaded_file)
    if isinstance(data, str): # Check if the load function returned an error message
        st.error(data)
        st.stop()
    st.sidebar.success("CSV file uploaded and processed successfully!")
else:
    data = regression_manager.get_default_data()
    st.sidebar.info("Using the default sample dataset. Upload a CSV to use your own data.")

# --- Main Panel for Displaying Results ---

# Train the model with the selected data
model, X, y = regression_manager.train_regression_model(data)

if model is None:
    st.warning("The dataset is empty or invalid. Please upload a valid CSV file.")
else:
    # Display the dataset
    st.subheader("📊 Dataset Used for Training")
    st.dataframe(data)

    st.markdown("---")
    
    # Display Model Performance
    st.subheader("⚙️ Model Performance")
    r2, equation = regression_manager.get_model_performance(model, X, y)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="R-squared Score", value=f"{r2:.2f}")
        st.info(
            "**R-squared** (from 0 to 1) shows how well the model explains the data. "
            "A score of 0.90 means 90% of the variation in marks can be explained by study hours."
        )
    with col2:
        st.write("**Regression Equation:**")
        st.latex(equation.replace(" ", "\\ ").replace("×", "\\times"))
        st.info(
            "This is the mathematical formula the model uses to make predictions."
        )

    st.markdown("---")

    # --- Prediction and Visualization Section ---
    st.subheader("🔮 Make a Prediction")
    
    col3, col4 = st.columns([1, 2])
    
    with col3:
        # User input for prediction
        user_hours = st.number_input("Enter Study Hours to Predict Marks:", min_value=0.0, max_value=24.0, value=5.0, step=0.5)
        
        # Get prediction
        predicted_marks = regression_manager.predict_marks(model, user_hours)
        
        st.success(f"Predicted Marks: **{predicted_marks:.2f}**")
    
    with col4:
        # Plotting
        st.write("**Visual Representation:**")
        fig, ax = plt.subplots()
        ax.scatter(X, y, color='blue', label='Actual Data')
        ax.plot(X, model.predict(X), color='red', linewidth=2, label='Regression Line')
        ax.scatter([user_hours], [predicted_marks], color='green', s=150, zorder=5, label='Your Prediction')
        
        ax.set_xlabel("Study Hours")
        ax.set_ylabel("Marks Obtained")
        ax.set_title("Study Hours vs. Marks")
        ax.legend()
        st.pyplot(fig)

# --- Footer ---
st.markdown("---")
st.caption("Made with ❤️ using Streamlit and Scikit-learn")


# program-3

# File Name: app.py
# This is the main application file that runs the Streamlit UI.

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import os

# Import your custom backend module
import ml_manager

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Interactive Classification Lab", layout="wide", page_icon="🔬")

# --- Sidebar for Navigation ---
st.sidebar.title("🔬 Navigation")
page = st.sidebar.radio("Go to", ["Upload & Clean Data", "Train & Evaluate Model", "Make a Prediction", "View History"])

# --- Initialize Session State ---
if 'df' not in st.session_state: st.session_state.df = None
if 'cleaned_df' not in st.session_state: st.session_state.cleaned_df = None
if 'model' not in st.session_state: st.session_state.model = None
if 'features' not in st.session_state: st.session_state.features = None
if 'label_encoders' not in st.session_state: st.session_state.label_encoders = None
if 'target_column' not in st.session_state: st.session_state.target_column = None

# =================================================================
# PAGE 1: UPLOAD AND CLEAN DATA
# =================================================================
if page == "Upload & Clean Data":
    st.title("1. Upload & Clean Your Dataset")
    
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file:
        df = ml_manager.load_data(uploaded_file)
        if isinstance(df, str):
            st.error(df)
        else:
            st.session_state.df = df
            st.success("File uploaded successfully!")
            st.dataframe(df.head())

    if st.session_state.df is not None:
        st.markdown("---")
        st.header("Data Cleaning Configuration")
        
        df_info = ml_manager.get_data_info(st.session_state.df)
        
        with st.expander("Show Dataset Information"):
            st.write(f"**Shape:** {df_info['shape']}")
            st.write("**Columns:**", df_info['columns'])
            st.write("**Missing Values:**")
            st.write(df_info['missing_values'][df_info['missing_values'] > 0])

        columns_to_drop = st.multiselect("Select columns to drop (optional):", df_info['columns'])
        
        st.subheader("Handle Missing Values")
        missing_value_strategies = {}
        for col in df_info['columns']:
            if df_info['missing_values'][col] > 0 and col not in columns_to_drop:
                strategy = st.selectbox(
                    f"Strategy for '{col}' ({df_info['missing_values'][col]} missing):",
                    ['Drop Rows', 'Fill with Mean', 'Fill with Median', 'Fill with Mode'],
                    key=f"strat_{col}"
                )
                missing_value_strategies[col] = strategy
        
        if st.button("Clean Data", type="primary"):
            with st.spinner("Cleaning data..."):
                cleaned_df, label_encoders = ml_manager.clean_data(st.session_state.df, columns_to_drop, missing_value_strategies)
                st.session_state.cleaned_df = cleaned_df
                st.session_state.label_encoders = label_encoders
                st.success("Data cleaned successfully!")
                st.write("Preview of Cleaned Data (after encoding):")
                st.dataframe(st.session_state.cleaned_df.head())

# =================================================================
# PAGE 2: TRAIN & EVALUATE MODEL
# =================================================================
elif page == "Train & Evaluate Model":
    st.title("2. Train & Evaluate a Classification Model")
    
    if st.session_state.cleaned_df is not None:
        st.info("Using the cleaned data from the previous step.")
        
        target_column = st.selectbox("Select the target column (what you want to predict):", st.session_state.cleaned_df.columns)
        
        if target_column:
            unique_values = st.session_state.cleaned_df[target_column].nunique()
            if unique_values > 10:
                st.warning(f"The column '{target_column}' has {unique_values} unique values. "
                           f"This might be a regression problem or require more advanced techniques. "
                           f"For best results, choose a target with fewer categories (e.g., 2-5).")
            elif unique_values > 2:
                 st.info(f"You've selected a multi-class target with {unique_values} categories.")
            else:
                 st.success(f"You've selected a binary target ('{target_column}'). This is ideal for classification!")

        model_name = st.selectbox("Select a classification model:", ["Logistic Regression", "Random Forest", "Support Vector Machine (SVM)"])
        
        if st.button("Train Model", type="primary"):
            with st.spinner(f"Training {model_name}..."):
                model, performance, features = ml_manager.train_classification_model(st.session_state.cleaned_df, target_column, model_name)
                
                if model:
                    st.session_state.model = model
                    st.session_state.features = features
                    st.session_state.target_column = target_column
                    st.success(f"{model_name} trained successfully!")
                    
                    st.header("📊 Model Performance")
                    st.metric("Accuracy Score", f"{performance['accuracy']:.2%}")
                    
                    st.subheader("Confusion Matrix")
                    fig, ax = plt.subplots()
                    labels = performance['labels']
                    if st.session_state.label_encoders.get(target_column):
                        labels = st.session_state.label_encoders[target_column].inverse_transform(labels)
                    
                    sns.heatmap(performance['conf_matrix'], annot=True, fmt='d', cmap='Blues', ax=ax, 
                                xticklabels=labels, yticklabels=labels)
                    plt.ylabel('Actual')
                    plt.xlabel('Predicted')
                    st.pyplot(fig)
                    
                    st.subheader("Classification Report")
                    report_df = pd.DataFrame(performance['class_report']).transpose()
                    st.dataframe(report_df)
                else:
                    st.error(performance)
    else:
        st.warning("Please upload and clean a dataset on the 'Upload & Clean Data' page first.")

# =================================================================
# PAGE 3: MAKE A PREDICTION
# =================================================================
elif page == "Make a Prediction":
    st.title("3. Make a Prediction")
    
    if st.session_state.model is not None:
        st.info("Enter the details below to get a prediction from the trained model.")
        
        input_data = {}
        original_df = st.session_state.df
        
        for feature in st.session_state.features:
            if feature in original_df.select_dtypes(include=np.number).columns:
                input_data[feature] = st.number_input(f"Enter value for '{feature}':", value=float(original_df[feature].mean()))
            else:
                unique_values = original_df[feature].dropna().unique().tolist()
                input_data[feature] = st.selectbox(f"Select value for '{feature}':", unique_values)

        if st.button("Predict", type="primary"):
            prediction, prediction_proba = ml_manager.make_prediction(
                st.session_state.model, st.session_state.features, input_data,
                st.session_state.label_encoders, original_df, st.session_state.target_column
            )
            
            st.success(f"**Predicted Outcome:** `{prediction}`")
            st.write("**Prediction Probabilities:**")
            
            class_labels = st.session_state.model.classes_
            if st.session_state.label_encoders.get(st.session_state.target_column):
                class_labels = st.session_state.label_encoders[st.session_state.target_column].inverse_transform(class_labels)
                
            st.write(dict(zip(class_labels, prediction_proba)))
            
    else:
        st.warning("Please train a model on the 'Train & Evaluate Model' page first.")

# =================================================================
# PAGE 4: VIEW HISTORY
# =================================================================
elif page == "View History":
    st.title("4. Training History")
    st.write("Here is a log of all the models you have trained.")
    
    history = ml_manager.load_training_history()
    if not history:
        st.info("No models have been trained yet.")
    else:
        history_df = pd.DataFrame(history)
        st.dataframe(history_df)
