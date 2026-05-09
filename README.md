# CRM Agent

An AI-powered CRM assistant that connects Google Gemini to Salesforce, delivered via Telegram and WhatsApp. Ask questions about deals, qualify leads, and get real-time Salesforce data - all from a chat message.

## What it does

- Look up deals and contacts live from Salesforce
- Qualify and score leads using BANT (potential for future: trained model to predict score)
- Work on Telegram and WhatsApp
- Powered by Google Gemini 1.5 Flash (free tier)

## Tech stack

-**AI:** Google Gemini 1.5 Flash (function calling) -**CRM:** Salesforce (simple-salesforce) -**Messaging:** Telegram Bot API + Twilio WhatsApp -**Backend:** FastAPI -**Language:** Python 3.10+

## Project Structure

'''bash
crm_agent/
|--- main.py # entry point
|--- agent/core.py # Gemini agent loop and function calling
|--- config/  
| |---settings.py # environment config
| |---prompts.py # system promot/agent persona
|--- integrations/
| |---salesforce.py # query + update Salesforce
| |---telegram.py # Telegram Bot API
| |---whatsapp.py # Twilion Wwhatsapp
|--- scoring/lead_scoring.py # BANT lead scoring (in the future, add XGBoost prediction module)
|--- memory/conversation.py # per-user chat history
|--- api/server.py # FastAPI webhooks
'''
