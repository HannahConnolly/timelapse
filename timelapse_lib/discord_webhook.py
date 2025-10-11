import os
import requests
from timelapse_lib.config import get_webhook_url


def send_discord_message(message, file_path=None):
    """Send a text message (and optional image) to Discord via webhook."""
    WEBHOOK_URL = get_webhook_url()
    if not WEBHOOK_URL:
        print("⚠️ No DISCORD_WEBHOOK_URL configured; skipping send. Message:", message)
        return

    print("➡️ Sending to Discord:", message)

    data = {"content": message}
    files = None

    if file_path:
        try:
            files = {"file": open(file_path, "rb")}
        except Exception as e:
            print(f"⚠️ Could not open file for upload: {e}")
            files = None

    try:
        response = requests.post(WEBHOOK_URL, data=data, files=files)
        if response.ok:
            print("✅ Sent to Discord")
        else:
            print(f"❌ Discord upload failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"⚠️ Error sending to Discord: {e}")
    finally:
        if files and files.get("file"):
            files["file"].close()
