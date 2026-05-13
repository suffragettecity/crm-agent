from twilio.rest import Client
from config.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM

def send_whatsapp(to: str, body: str) -> str:
    """
    Send a WhatsApp message via Twilio. 
    'to' must be in format  whatsapp +971501234567
    """
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        to=to,
        body=body,
    )
    return message.sid