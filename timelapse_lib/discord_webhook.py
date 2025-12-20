import requests
from timelapse_lib.config import get_photo_webhook_url, get_ai_webhook_url
from .gemini import send_to_gemini

def _execute_webhook(webhook_url, message, file_path=None):
    """Internal helper to handle the actual network request."""
    if not webhook_url:
        print(f"⚠️ Webhook URL missing. Cannot send: {message[:30]}")
        return

    data = {"content": message}
    files = None

    try:
        if file_path:
            files = {"file": open(file_path, "rb")}
        
        response = requests.post(webhook_url, data=data, files=files, timeout=10)
        
        if response.ok:
            print(f"✅ Successfully posted to Discord")
        else:
            print(f"❌ Discord error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"⚠️ Request error: {e}")
    finally:
        if files:
            files["file"].close()


def send_discord_message_in_photo_channel(message, file_path=None):
    url = get_photo_webhook_url()
    _execute_webhook(url, message, file_path)

def send_discord_message_in_ai_channel(message, file_path=None):
    url = get_ai_webhook_url()
    message = send_to_gemini()
    message = f"🤖 AI Analysis:\n```json\n{message}\n```"
    _execute_webhook(url, message, file_path)