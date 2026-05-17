from fastapi import FastAPI, Request, Form
from fastapi.responses import Response

from agent.core import run_agent
from memory.conversation import get_history, save_history, clear_history
from integrations.telegram import send_message as tg_send
from integrations.whatsapp import send_whatsapp

app = FastAPI(title="Gonn CRM Agent")

# Health check
@app.get("/")
def root():
    return {"status": "Gonn CRM Agent is running"}

# Telegram webhook

@app.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()

    # Extract message
    message = data.get("message") or data.get("edited_message")
    if not message:
        return {"ok": True}
    
    chat_id = message["chat"]["id"]
    user_message = message.get("text", "")

    if not user_message:
        return {"ok": True}
    
    # Special command: /reset clears conversation history
    if user_message.strip().lower() == "/reset":
        clear_history(chat_id)
        await tg_send(chat_id, "Conversation cleared. Start fresh!")
        return {"ok": True}
    
    # Load history
    history = get_history(chat_id)
    reply = run_agent(user_message, history)
    save_history(chat_id, history)

    await tg_send(chat_id, reply)
    return {"ok": True}

