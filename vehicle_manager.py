# File Name: vehicle_manager.py
# This module contains all the backend logic for the AI Vehicle Recommender.

import google.generativeai as genai
import re
import requests
from bs4 import BeautifulSoup
import json

def get_image_from_google(query: str) -> str:
    """
    Scrapes Google Images for a given query and returns the URL of the first image.
    """
    # A fallback image in case scraping fails
    fallback_image = "https://via.placeholder.com/400x300.png?text=Image+Not+Found"
    
    try:
        # We add "official image" to get better results
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}+official+image&tbm=isch"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all image tags
        image_tags = soup.find_all('img')
        
        # Find the first valid, non-base64 image URL
        for img in image_tags:
            if img.get('src') and img['src'].startswith('https://'):
                return img['src']
        
        return fallback_image
    except Exception as e:
        print(f"Error scraping image for '{query}': {e}")
        return fallback_image


def call_gemini_for_vehicles(api_key: str, prompt: str) -> list | str:
    """
    Calls the Gemini API and parses the response into a structured list of dictionaries.
    """
    try:
        genai.configure(api_key=api_key)
        
        # UPDATED system instruction to ask for JSON output WITHOUT image URL
        system_instruction = """
You are a vehicle expert AI assistant. Your goal is to suggest 2-3 vehicles.
Provide your response as a valid JSON array of objects. Each object must contain these exact keys: "model_name", "brand", "price_inr", "fuel_type", "transmission", "seating", "reason".
For 2-wheelers, set "transmission" and "seating" to "N/A".
Do NOT include any text or formatting outside of the JSON array.

Example response:
[
  {
    "model_name": "Hero Splendor Plus",
    "brand": "Hero MotoCorp",
    "price_inr": "70,000",
    "fuel_type": "Petrol",
    "transmission": "N/A",
    "seating": "N/A",
    "reason": "A reliable, fuel-efficient, and affordable commuter motorcycle."
  }
]
"""
        
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction
        )
        
        response = model.generate_content(prompt)
        
        # --- NEW PARSING LOGIC FOR JSON ---
        recommendations = []
        # Clean the response to get only the JSON part
        json_text = response.text.strip().replace("```json", "").replace("```", "")
        vehicle_data = json.loads(json_text)
        
        for vehicle in vehicle_data:
            # Now, we fetch the image for each vehicle
            image_query = f"{vehicle.get('brand', '')} {vehicle.get('model_name', '')}"
            image_url = get_image_from_google(image_query)
            
            # Combine AI text with the scraped image URL
            recommendations.append({
                "data": vehicle,
                "image_url": image_url
            })
                
        return recommendations if recommendations else "Sorry, I couldn't generate a valid recommendation. Please try again."

    except json.JSONDecodeError:
        return "❌ **Error:** The AI returned an invalid format. Please try your request again."
    except Exception as e:
        if "API key not valid" in str(e):
            return "❌ **Error:** Your Gemini API key is not valid."
        else:
            return f"❌ **An unexpected error occurred:** {str(e)}"

def recommend_2wheeler(api_key, fuel, budget, brand, usage, look, extra):
    """Builds a prompt and gets recommendations for a 2-wheeler."""
    prompt = f"Recommend 2-wheelers: Fuel={fuel}, Budget=₹{budget:,}, Brand={brand}, Usage={usage}, Style={look or 'Any'}, Other={extra or 'None'}"
    return call_gemini_for_vehicles(api_key, prompt)

def recommend_4wheeler(api_key, fuel, budget, brand, seating, usage, transmission, look, extra):
    """Builds a prompt and gets recommendations for a 4-wheeler."""
    prompt = f"Recommend 4-wheelers: Fuel={fuel}, Budget=₹{budget:,}, Brand={brand}, Seating={seating}, Usage={usage}, Transmission={transmission}, Style={look or 'Any'}, Other={extra or 'None'}"
    return call_gemini_for_vehicles(api_key, prompt)

def ask_anything(api_key, custom_prompt):
    """Handles a general, free-form question about vehicles."""
    return call_gemini_for_vehicles(api_key, custom_prompt)
