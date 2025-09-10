# File Name: motivation_manager.py
# This module contains all the backend logic for the Motivation Buddy app.

import os
import json
import random
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# --- Constants ---
USER_DATA_FILE = "user_streaks.json"

# ------------------------------------------------------------------
# 1. DATA STORAGE FUNCTIONS
# ------------------------------------------------------------------
def load_user_data():
    """Load user streak data from JSON file"""
    if not os.path.exists(USER_DATA_FILE):
        return {}
    try:
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading user data: {e}")
        return {}

def save_user_data(data):
    """Save user streak data to JSON file"""
    try:
        with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Error saving user data: {e}")

def update_user_streak(user_name):
    """Update user's motivation streak and return relevant stats"""
    if not user_name.strip():
        return 0, 0, 1 # current_streak, best_streak, total_interactions
    
    data = load_user_data()
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    if user_name not in data:
        data[user_name] = {
            "current_streak": 1, "best_streak": 1,
            "last_interaction": today_str, "total_interactions": 1
        }
    else:
        user = data[user_name]
        last_date = datetime.strptime(user["last_interaction"], "%Y-%m-%d")
        today_date = datetime.strptime(today_str, "%Y-%m-%d")
        
        delta = (today_date - last_date).days
        if delta == 1:
            user["current_streak"] += 1
            user["total_interactions"] += 1
        elif delta > 1:
            user["current_streak"] = 1
            user["total_interactions"] += 1
        elif delta == 0 and user.get("total_interactions", 0) == 0:
             # First interaction of the day
             user["total_interactions"] += 1

        user["best_streak"] = max(user["current_streak"], user["best_streak"])
        user["last_interaction"] = today_str

    save_user_data(data)
    user_info = data[user_name]
    return user_info["current_streak"], user_info["best_streak"], user_info["total_interactions"]

# ------------------------------------------------------------------
# 2. MOTIVATIONAL CONTENT FUNCTIONS
# ------------------------------------------------------------------
def get_motivation_from_web():
    """Scrape a motivational quote from the web with a reliable fallback."""
    fallback_quotes = [
        {"quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
        {"quote": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "author": "Winston Churchill"}
    ]
    try:
        url = "https://www.brainyquote.com/quote_of_the_day"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        quote_elem = soup.select_one(".qotd-q-text, .qotd-quote")
        author_elem = soup.select_one(".qotd-q-author, .qotd-author")
        
        if quote_elem and author_elem:
            quote = quote_elem.get_text(strip=True).replace('"', '')
            author = author_elem.get_text(strip=True).replace(',', '').replace('―', '').strip()
            return {"quote": quote, "author": author}
    except requests.RequestException as e:
        print(f"Error scraping quote: {e}")
    
    return random.choice(fallback_quotes)

def get_affirmation(mood, streak=0):
    """Get a mood-based affirmation, enhanced with streak info."""
    affirmations = {
        "Happy": "Your positive energy is infectious! Keep spreading joy! ✨",
        "Sad": "You are stronger than you think, and this feeling will pass. 💪",
        "Stressed": "Breathe deeply. You've handled 100% of your worst days so far. 🧘‍♀️",
        "Motivated": "Channel that fire! You're unstoppable when you set your mind to it! 🔥",
        "Neutral": "Today is a blank canvas - paint it with your dreams! 🎨",
        "Anxious": "Anxiety is temporary, but your strength is permanent. 🛡️",
        "Tired": "Rest is not a reward, but a requirement. Give yourself permission to rest. 😴"
    }
    base_affirmation = affirmations.get(mood, affirmations["Neutral"])
    
    if streak > 1:
        return f"{base_affirmation}\n\n**Bonus:** You're on a {streak}-day streak! Keep the momentum going! 🔥"
    return base_affirmation

def get_productivity_badge(streak, total_interactions):
    """Generate a descriptive badge based on user activity."""
    if streak >= 30: return "🏆 Consistency Legend"
    if streak >= 7: return "⭐ Week Champion"
    if streak >= 3: return "🚀 Momentum Builder"
    if total_interactions >= 50: return "🎯 Half-Century Hero"
    if total_interactions >= 10: return "⚡ Active Achiever"
    return "🌱 Fresh Start"

# ------------------------------------------------------------------
# 3. GEMINI AI CHATBOT LOGIC
# ------------------------------------------------------------------
def build_prompt(user_question, quote, affirmation, badge, user_name, mood, streak):
    """Build a comprehensive and structured prompt for the Gemini AI."""
    return f"""
You are a warm, encouraging, and highly motivating personal coach.

**USER's CONTEXT:**
- Name: {user_name if user_name else "Friend"}
- Current Mood: {mood}
- Motivation Streak: {streak} days
- Current Badge: {badge}
- Today's Quote for Inspiration: "{quote['quote']}" — {quote['author']}
- Personal Affirmation for Today: "{affirmation}"

**USER's REQUEST:**
"{user_question}"

**YOUR TASK:**
1.  Acknowledge their request and mood in a warm, conversational tone.
2.  If their streak is greater than 1, congratulate them on their consistency.
3.  Provide practical, actionable advice directly related to their request.
4.  Keep the response concise, positive, and structured (e.g., use bullet points for tips).
5.  End with an encouraging and uplifting closing statement.
"""

def get_ai_response(api_key, user_message, mood, user_name):
    """The main chatbot function that orchestrates all backend logic."""
    try:
        genai.configure(api_key=api_key)
        
        current_streak, _, total_interactions = update_user_streak(user_name)
        
        quote = get_motivation_from_web()
        affirmation = get_affirmation(mood, current_streak)
        badge = get_productivity_badge(current_streak, total_interactions)
        
        prompt = build_prompt(user_message, quote, affirmation, badge, user_name, mood, current_streak)
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text or "I'm here to help! Could you please rephrase your question?"

    except Exception as e:
        print(f"Error in get_ai_response: {e}")
        return (
            "I'm experiencing some technical difficulties, but I'm still here for you! 🤗\n\n"
            "**Today's Affirmation:** Challenges are just opportunities in disguise!"
        )

def get_user_stats(user_name):
    """Get formatted user statistics for display."""
    if not user_name.strip():
        return "Enter your name to track your progress! 📊"
    
    data = load_user_data().get(user_name)
    if not data:
        return f"Welcome {user_name}! Start your motivation journey today! 🌟"
    
    return f"""
    ### 📊 **{user_name}'s Progress:**
    - **Current Streak:** {data['current_streak']} days 🔥
    - **Best Streak:** {data['best_streak']} days 🏆
    - **Total Interactions:** {data['total_interactions']} 💬
    - **Last Active:** {data['last_interaction']} 📅
    """
