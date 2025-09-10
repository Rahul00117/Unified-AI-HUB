# File Name: utility_manager.py
# This module contains all the backend logic for the AI Automation Hub app.

import os
import smtplib
from email.message import EmailMessage
import pywhatkit as kit
from twilio.rest import Client as TwilioClient
import tweepy
from instagrapi import Client as InstaClient
import requests
from bs4 import BeautifulSoup

# --- Communication Functions ---

def send_whatsapp_pywhatkit(number, message, hour, minute):
    """Schedules a WhatsApp message using pywhatkit."""
    kit.sendwhatmsg(number, message, hour, minute, wait_time=15, tab_close=True)

def send_email_gmail(subject, body, to_email, from_email, password):
    """Sends an email using Gmail's SMTP server."""
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(from_email, password)
        server.send_message(msg)

def send_whatsapp_twilio(account_sid, auth_token, from_whatsapp, to_whatsapp, message):
    """Sends a WhatsApp message using the Twilio API."""
    client = TwilioClient(account_sid, auth_token)
    client.messages.create(
        body=message,
        from_=f'whatsapp:{from_whatsapp}',
        to=f'whatsapp:{to_whatsapp}'
    )

def send_sms_twilio(account_sid, auth_token, from_number, to_number, message):
    """Sends an SMS using the Twilio API."""
    client = TwilioClient(account_sid, auth_token)
    client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    )

def make_call_twilio(account_sid, auth_token, from_number, to_number, twiml_url):
    """Initiates a phone call using the Twilio API."""
    client = TwilioClient(account_sid, auth_token)
    client.calls.create(
        to=to_number,
        from_=from_number,
        url=twiml_url
    )

# --- Social Media and Web Functions ---

def search_google(query):
    """Performs a Google search and returns the page title."""
    url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    response.raise_for_status() # Raise an exception for bad status codes
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.title.string

def post_to_instagram(username, password, image_path, caption):
    """Logs into Instagram and uploads a photo with a caption."""
    cl = InstaClient()
    cl.login(username, password)
    cl.photo_upload(image_path, caption)

def post_to_twitter(api_key, api_secret, access_token, access_secret, text):
    """Posts a new tweet (status update) to Twitter/X."""
    # This uses Twitter API v1.1 which is common for many libraries
    auth = tweepy.OAuth1UserHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    api.update_status(status=text)

def scrape_website_html(url):
    """Scrapes the full HTML content of a given URL."""
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.prettify()
