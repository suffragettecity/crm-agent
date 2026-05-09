import os
from dotenv import load_dotenv

load_dotenv()

# Google Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = "gemini-1.5-flash"          # free tier

# Salesforce
SF_USERNAME = os.getenv("SF_USERNAME")
SF_PASSWORD = os.getenv("SF_PASSWORD")
SF_SECURITY_TOKEN = os.getenv("SF_SECURITY_TOKEN")

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# WhatsApp via Twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")

# Agent behavior
MAX_AGENT_TURNS = 6         # safety limit on the reasoning loop
MAX_HISTORY_MESSAGES = 20   # messages to keep per user session 