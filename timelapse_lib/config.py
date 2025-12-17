import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTOS_DIR = os.path.join(BASE_DIR, "photos")
GIFS_DIR = os.path.join(BASE_DIR, "gifs")


def load_secrets():
    """Return a dict of secrets loaded from environment and `.env`.

    Precedence (highest -> lowest): system environment variables,
    `.env` file in project root. This intentionally omits `secrets.json`.
    """
    data = {}

    # Highest precedence: explicit environment variables
    env_val = os.environ.get("DISCORD_WEBHOOK_URL")
    if env_val:
        data["DISCORD_WEBHOOK_URL"] = env_val

    # Next: parse a .env file in the project root (simple KEY=VALUE parser)
    dotenv_path = os.path.join(BASE_DIR, ".env")
    if os.path.exists(dotenv_path):
        try:
            with open(dotenv_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    # only set if not already provided via environment
                    if k not in data:
                        data[k] = v
        except Exception:
            # ignore parse errors
            pass

    return data


def get_webhook_url():
    return load_secrets().get("DISCORD_WEBHOOK_URL")
