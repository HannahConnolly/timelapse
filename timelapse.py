import cv2
import requests
import datetime
import traceback
import os
import glob
import json


# Reduce OpenCV log noise (GStreamer warnings) when possible. This hides
# non-fatal backend warnings like "Cannot query video position".
try:
    # new-style logging API
    cv2.utils.logging.setLogLevel(cv2.utils.logging.LOG_LEVEL_ERROR)
except Exception:
    # Older OpenCV builds may not have the utils.logging API; ignore.
    pass


# Load webhook URL from environment or a secrets file. This keeps sensitive
# information out of source control. Create a `secrets.json` next to this file
# with the shape: { "DISCORD_WEBHOOK_URL": "https://..." }
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _load_webhook_url():
    # 1) prefer env var
    env = os.environ.get("DISCORD_WEBHOOK_URL")
    if env:
        return env

    # 2) try secrets.json in repo root (next to this file)
    secrets_path = os.path.join(BASE_DIR, "secrets.json")
    if os.path.exists(secrets_path):
        try:
            with open(secrets_path, "r") as f:
                data = json.load(f)
            return data.get("DISCORD_WEBHOOK_URL")
        except Exception as e:
            print(f"⚠️ Could not read secrets.json: {e}")

    # not configured
    return None


WEBHOOK_URL = _load_webhook_url()

# Directory where photos will be saved/read from (relative to this script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTOS_DIR = os.path.join(BASE_DIR, "photos")


def send_discord_message(message, file_path=None):
    """Send a text message (and optional image) to Discord via webhook.

    file_path can be a relative or absolute path. If provided, this function
    will verify the file exists before attempting upload.
    """
    if not WEBHOOK_URL:
        print("⚠️ No DISCORD_WEBHOOK_URL configured; skipping send. Message:", message)
        return

    data = {"content": message}
    files = None

    if file_path:
        # Normalize and verify
        file_path = os.path.abspath(file_path)
        if not os.path.exists(file_path):
            print(f"⚠️ File not found, won't attach: {file_path}")
            file_path = None
        else:
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

def capture_photo():
    """Capture a single image from the webcam and save it under `photos/`.

    Returns the absolute path to the saved image.
    """
    # ensure photos dir exists
    os.makedirs(PHOTOS_DIR, exist_ok=True)

    # Try to prefer the v4l2 backend for local webcams (reduces gstreamer noise
    # and is usually more reliable on Linux). If it's not available, fall back
    # to the default backend.
    cap = None
    try:
        if hasattr(cv2, 'CAP_V4L2'):
            cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    except Exception:
        cap = None

    if cap is None or not cap.isOpened():
        # fallback to default backend
        cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        send_discord_message(f"⚠️ Could not open webcam at {datetime.datetime.now()}")
        raise RuntimeError("Could not open webcam.")

    ret, frame = cap.read()
    cap.release()

    if not ret:
        send_discord_message(f"⚠️ Could not read frame from webcam at {datetime.datetime.now()}")
        raise RuntimeError("Could not read frame from webcam.")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"photo_{timestamp}.jpg"
    full_path = os.path.join(PHOTOS_DIR, filename)
    cv2.imwrite(full_path, frame)
    print(f"Saved image to {full_path}")
    return full_path


def get_latest_photo():
    """Return the absolute path to the most recently modified photo in `photos/`, or None if none exist."""
    if not os.path.isdir(PHOTOS_DIR):
        return None

    patterns = [os.path.join(PHOTOS_DIR, "*.jpg"), os.path.join(PHOTOS_DIR, "*.png")]
    files = []
    for p in patterns:
        files.extend(glob.glob(p))

    if not files:
        return None

    latest = max(files, key=os.path.getmtime)
    return os.path.abspath(latest)

def main():
    print("init timelapse")
    send_discord_message("📸 Taking photo...")

    try:
        filename = capture_photo()
        send_discord_message(f"✅ Captured photo on {datetime.datetime.now().strftime('%m/%d')}", file_path=filename)
    except Exception as e:
        error_msg = f"❌ Error during capture:\n```\n{traceback.format_exc()}\n```"
        print(error_msg)
        send_discord_message(error_msg)

if __name__ == "__main__":
    main()
