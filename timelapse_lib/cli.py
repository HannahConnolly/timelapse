from .capture import capture_photo
from .discord_webhook import send_discord_message
from .disk_stats import get_free_space_gb_str
import datetime
import traceback


def main():
    print("init timelapse")
    send_discord_message("📸 Taking photo...")

    try:
        filename = capture_photo()
        disk_space = get_free_space_gb_str("/")
        send_discord_message(f"✅ Captured photo on {datetime.datetime.now().strftime('%m/%d')} - {disk_space}", file_path=filename)
    except Exception as e:
        error_msg = f"❌ Error during capture:\n```\n{traceback.format_exc()}\n```"
        print(error_msg)
        send_discord_message(error_msg)
