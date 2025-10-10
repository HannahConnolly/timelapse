# Timelapse

Simple timelapse helper that captures a single photo from the local webcam and saves images to the `photos/` folder. Optionally sends a notification (and the photo) to a Discord webhook.

## What this repo contains
- `timelapse.py` - main script. Exposes `capture_photo()` and `get_latest_photo()` and a `main()` runner that captures one photo and (optionally) posts to Discord.
- `photos/` - directory where captured images are stored (created automatically by the script).
- `secrets.json.example` - example file showing how to store your Discord webhook URL out of source control.
- `requirements.txt` - Python packages required to run the script.

## Requirements
- Python 3.8+
- A working webcam available to the OS (typically `/dev/video0` on Linux).
- pip to install dependencies.

On Debian/Ubuntu you may also want the v4l-utils and GStreamer plugins for best camera support:

```bash
sudo apt update
sudo apt install -y v4l-utils gstreamer1.0-tools gstreamer1.0-libav \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad
```

## Install

Create a virtualenv (recommended) and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration (secrets)

The script reads your Discord webhook in one of two ways (in order):

- `DISCORD_WEBHOOK_URL` environment variable
- `secrets.json` file placed next to `timelapse.py` with JSON like:

```json
{
  "DISCORD_WEBHOOK_URL": "https://discord.com/api/webhooks/..."
}
```

To get started, copy the example and fill in your webhook:

```bash
cp secrets.json.example secrets.json
# edit secrets.json and paste your webhook
```

Note: `secrets.json` should NOT be committed. Add it to `.gitignore` if it's not already ignored.

## Run

Capture a single photo (and post to Discord if configured):

```bash
python3 timelapse.py
```

If you only want to run without posting to Discord, either unset the `DISCORD_WEBHOOK_URL` env var or remove/rename `secrets.json`.

If you find the GStreamer warnings noisy, the script attempts to reduce OpenCV logging. You can also suppress stderr entirely (hides warnings and errors):

```bash
python3 timelapse.py 2>/dev/null
```

## Troubleshooting

- "Cannot query video position" warnings are usually harmless for live cameras. The script prefers the `v4l2` backend on Linux which reduces those messages.
- If the camera cannot be opened: check permissions for `/dev/video0` and run `v4l2-ctl --list-devices`.
- If frame capture fails (no image saved), try running a short test program or `ffmpeg`/`v4l2-ctl` to verify the device works.

## File layout

```
timelapse.py
photos/             # captured images
secrets.json.example
requirements.txt
README.md
```

## Next steps / ideas
- Add CLI flags to change camera index and disable Discord posting at runtime.
- Add a scheduler loop to capture every N minutes and rotate old images.
- Add unit tests for filesystem helpers.

If you want, I can add a simple scheduler or argument parsing next.

---
Happy timelapsing!
