import httpx
from config.settings import TELEGRAM_TOKEN

TELEGRAM_API=f""

async def send_message(chat_id: int|str,text:str)-> None:
    """Send a text message to a Telegram chat"""
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown", # use bold/italics in replies
            },
        )

async def set_webhook(url:str)->dict:
    """Register the webhook URL with telegram (call once on deploy)."""
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{TELEGRAM_API}/setWebhook",
            json={"url":url},
        )
        return r.json()