from .capture import capture_photo
from .discord_webhook import send_discord_message
from .disk_stats import get_free_space_gb_str
from .create_gif import create_gif
import datetime
import traceback
import argparse


def init_argparse():
    parser = argparse.ArgumentParser(description='Capture timelapse photos')
    parser.add_argument('-d', '--discord', action='store_true', help='Send Discord notifications')
    parser.add_argument('-g', '--gif', action='store_true', help='Create animated GIF from captured photos')
    parser.add_argument('-m', '--gif-ms', type=int, default=150, metavar='MS', help='Frame duration in milliseconds for GIF (default: 100)')
    return parser


def main(argv):
    parser = init_argparse()
    args = parser.parse_args(argv)
    if args.gif:
        call_create_gif(args)
    else:
        call_take_photo(args)

def call_take_photo(args):
    if args.discord:
        send_discord_message("📸 Taking photo...")

    try:
        disk_space = get_free_space_gb_str("/")
        if not args.gif:
            filename = capture_photo()
            if args.discord:
                send_discord_message(f"✅ Captured photo on {datetime.datetime.now().strftime('%m/%d')} - {disk_space}", file_path=filename)
    except Exception as e:
        error_msg = f"❌ Error during capture:\n```\n{traceback.format_exc()}\n```"
        if args.discord:
            send_discord_message(error_msg)
        print(error_msg)

def call_create_gif(args):
    try:
        output_gif = create_gif(gif_ms=args.gif_ms)
        if args.discord:
            send_discord_message("✅ Created timelapse GIF", file_path=output_gif)
    except Exception as e:
        error_msg = f"❌ Error during capture:\n```\n{traceback.format_exc()}\n```"
        if args.discord:
            send_discord_message(error_msg)
        print(error_msg)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])