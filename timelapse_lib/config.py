import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTOS_DIR = os.path.join(BASE_DIR, "photos")
GIFS_DIR = os.path.join(BASE_DIR, "gifs")


def load_secrets():
    """Return a dict of secrets loaded from DISCORD_WEBHOOK_URL env var or secrets.json."""
    data = {}
    env = os.environ.get("DISCORD_WEBHOOK_URL")
    if env:
        data["DISCORD_WEBHOOK_URL"] = env

    secrets_path = os.path.join(BASE_DIR, "secrets.json")
    if os.path.exists(secrets_path):
        try:
            with open(secrets_path, "r") as f:
                file_data = json.load(f)
            data.update(file_data)
        except Exception:
            # keep silent; caller will handle absence
            pass

    return data


def get_webhook_url():
    return load_secrets().get("DISCORD_WEBHOOK_URL")
