# File Name: saundarya_manager.py
# This module contains all the backend logic for the Saundarya Lite app.

import os
import re
import uuid
import datetime
from pathlib import Path
import pandas as pd
from PIL import Image
import google.generativeai as genai
import streamlit as st

# --- Constants for Data Storage ---
CSV_FILE = "fashion_log.csv"
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# ------------------------------------------------------------------
# GEMINI HELPERS
# ------------------------------------------------------------------
def call_gemini(api_key: str, prompt: str, image: Image.Image) -> str:
    """Call Gemini API with proper error handling"""
    try:
        # Re-configure the API key for this call
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([prompt, image])
        return response.text or "No response generated"
    except Exception as e:
        st.error(f"Gemini API Error: {e}")
        return generate_mock_response(prompt)

def generate_mock_response(prompt: str) -> str:
    """Generate a more detailed mock response for demo purposes."""
    return """
**Gender**: Female
**Mood**: Confident
**Skin Tone**: Medium
**Upper Wear Color**: Blue
**Lower Wear Color**: Black
**Outfit Style**: Business Casual
**Fit Assessment**: Well-fitted
**Pattern**: Solid Colors
**Fabric Suggestion**: Cotton Blend for the top, Denim for the bottom.
**Overall Vibe**: Professional and stylish
**Accessory Recommendations**:
• A simple silver necklace to complement the neckline.
• A classic leather belt to define the waist.
• Black pointed-toe heels to elongate the legs.
**Fashion Tips**: 
• Consider adding a statement blazer to elevate the look for a more formal meeting.
• The color combination works well for your skin tone, creating a balanced and professional appearance.
• Rolling up the sleeves slightly can add a touch of relaxed sophistication.
**Confidence Score**: 8/10
    """

def parse_gemini_response(text: str) -> dict:
    """Parse Gemini response into structured data, now handling lists."""
    fields = [
        "Gender", "Mood", "Skin Tone", "Upper Wear Color", 
        "Lower Wear Color", "Outfit Style", "Fit Assessment", "Pattern",
        "Fabric Suggestion", "Overall Vibe", "Accessory Recommendations", 
        "Fashion Tips", "Confidence Score"
    ]
    
    result = {field: "N/A" for field in fields}
    
    for field in fields:
        # Regex to capture content between a field and the next field or end of string
        pattern = rf"\*\*{re.escape(field)}\*\*\s*:?\s*(.*?)(?=\s*\*\*|$)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            value = match.group(1).strip()
            
            # If the value contains bullet points, format it as a list
            if '•' in value:
                # Split by bullet, strip whitespace, and filter out empty strings
                items = [item.strip() for item in value.split('•') if item.strip()]
                # Join with a newline character for clean storage and display
                result[field] = "\n".join(f"• {item}" for item in items)
            else:
                # Clean up single-line values
                value = re.sub(r'\n+', ' ', value)
                value = re.sub(r'\s+', ' ', value)
                result[field] = value
    
    return result

# ------------------------------------------------------------------
# DATA STORAGE FUNCTIONS
# ------------------------------------------------------------------
def save_analysis_result(features: dict, image_path: str, occasion: str):
    """Save analysis result to CSV file"""
    try:
        record = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "image_path": image_path,
            "occasion": occasion,
            **features
        }
        
        df = pd.DataFrame([record])
        file_exists = os.path.isfile(CSV_FILE)
        df.to_csv(CSV_FILE, mode="a", index=False, header=not file_exists)
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

def load_fashion_history():
    """Load fashion history from CSV file"""
    try:
        if os.path.isfile(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading history: {e}")
        return pd.DataFrame()

def save_image(image: Image.Image) -> str:
    """Save uploaded image and return the file path"""
    try:
        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = UPLOAD_DIR / filename
        
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        
        image.save(filepath, "JPEG", quality=85)
        return str(filepath)
    except Exception as e:
        st.error(f"Error saving image: {e}")
        return ""
