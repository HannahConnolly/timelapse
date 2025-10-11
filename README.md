
# Timelapse

Lightweight helper to capture a single photo from a local webcam and store images in the `photos/` folder. Optionally posts messages (and images) to a Discord webhook.

This repository is structured as a small package so you can reuse the core functionality from other scripts or tests:

- `timelapse.py` — tiny entry point that calls `timelapse_lib.cli.main()`
- `timelapse_lib/` — package containing the main implementation:
  - `capture.py` — capture helpers (`capture_photo()`, `get_latest_photo()`)
  - `discord_webhook.py` — helper to send messages and optional files to Discord
  - `config.py` — secret/loading helpers
  - `disk_stats.py` — small disk space helper used by the notifier
- `photos/` — directory where captured images are stored (created automatically)
- `secrets.json.example` — example secrets file showing the expected JSON format
- `requirements.txt` — external Python dependencies

## Requirements

- Python 3.8+ (3.11 used during development)
- A working webcam accessible to the OS (typically `/dev/video0` on Linux)
- pip to install dependencies

On Debian/Ubuntu you may want to install v4l-utils and GStreamer plugins for best camera support:

```bash
sudo apt update
sudo apt install -y v4l-utils gstreamer1.0-tools gstreamer1.0-libav \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad
```

## Install

Create and activate a virtual environment, then install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration (Discord webhook)

The code will look for a webhook URL in this order:

1. `DISCORD_WEBHOOK_URL` environment variable
2. `secrets.json` file located next to the package root (see `secrets.json.example`)

Example `secrets.json` content:

```json
{
  "DISCORD_WEBHOOK_URL": "https://discord.com/api/webhooks/your_webhook_id/your_webhook_token"
}
```

To create your own local secrets file from the example:

```bash
cp secrets.json.example secrets.json
# then edit secrets.json and paste your webhook URL
```

Note: Do NOT commit `secrets.json` to version control. Add it to `.gitignore` if needed.

## Usage

Capture a single photo and (optionally) post to Discord:

```bash
python3 timelapse.py
```

If you don't want any Discord posting, either unset the `DISCORD_WEBHOOK_URL` environment variable or remove/rename `secrets.json`.

To reduce noisy OpenCV/GStreamer warnings you can suppress stderr:

# Timelapse

Lightweight helper that captures a single photo from a local webcam and stores images in the `photos/` folder. Optionally posts messages (and images) to a Discord webhook.

This project is organised as a small package so core functionality can be reused from other scripts or tests.

Repository contents

- `timelapse.py` — entry point which calls `timelapse_lib.cli.main()`
- `timelapse_lib/` — core package:
  - `capture.py` — capture helpers (`capture_photo()`, `get_latest_photo()`)
  - `discord_webhook.py` — send messages/files via Discord webhook
  - `config.py` — secrets loading (env var or `secrets.json`)
  - `disk_stats.py` — small helper used in notifications
- `photos/` — where captured images are stored (created automatically)
- `secrets.json.example` — example secrets file
- `requirements.txt` — Python dependencies

## Requirements

- Python 3.8+ (development used 3.11)
- A working webcam (e.g. `/dev/video0` on Linux)
- pip

On Debian/Ubuntu you may want to install `v4l-utils` and GStreamer plugins for best camera support:

```bash
sudo apt update
sudo apt install -y v4l-utils gstreamer1.0-tools gstreamer1.0-libav \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad
```

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration (Discord webhook)

The webhook URL is resolved in this order:

1. `DISCORD_WEBHOOK_URL` environment variable
2. `secrets.json` file placed next to the project root (see `secrets.json.example`)

Example `secrets.json`:

```json
{
  "DISCORD_WEBHOOK_URL": "https://discord.com/api/webhooks/your_webhook_id/your_webhook_token"
}
```

Create a local secrets file from the example:

```bash
cp secrets.json.example secrets.json
# then edit secrets.json and paste your webhook URL
```

Do not commit `secrets.json`.

## Usage

Capture a single photo (and post to Discord if configured):

```bash
python3 timelapse.py
```

If you want to run without Discord, unset `DISCORD_WEBHOOK_URL` or remove/rename `secrets.json`.

To silence OpenCV/GStreamer warnings:

```bash
python3 timelapse.py 2>/dev/null
```

## Development notes

- `capture_photo(device=0, warmup_seconds=10)` will warm up the camera for the given seconds then save an image to `photos/`.
- `timelapse_lib.config.load_secrets()` prefers the environment variable and falls back to `secrets.json`.
- `timelapse_lib.discord_webhook.send_discord_message()` no-ops (with a printed warning) if no webhook is configured so you can run locally.

# Timelapse

Lightweight helper that captures a single photo from a local webcam and saves images to the `photos/` folder. Optionally posts messages (and images) to a Discord webhook.

This project is organised as a small package so core functionality can be reused from other scripts or tests.

Repository contents

- `timelapse.py` — entry point which calls `timelapse_lib.cli.main()`
- `timelapse_lib/` — core package:
  - `capture.py` — capture helpers (`capture_photo()`, `get_latest_photo()`)
  - `discord_webhook.py` — send messages/files via Discord webhook
  - `config.py` — secrets loading (env var or `secrets.json`)
  - `disk_stats.py` — small helper used in notifications
- `photos/` — where captured images are stored (created automatically)
- `secrets.json.example` — example secrets file
- `requirements.txt` — Python dependencies

## Requirements

- Python 3.8+ (development used 3.11)
- A working webcam (e.g. `/dev/video0` on Linux)
- pip

On Debian/Ubuntu you may want to install `v4l-utils` and GStreamer plugins for best camera support:

```bash
sudo apt update
sudo apt install -y v4l-utils gstreamer1.0-tools gstreamer1.0-libav \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad
```

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration (Discord webhook)

The webhook URL is resolved in this order:

1. `DISCORD_WEBHOOK_URL` environment variable
2. `secrets.json` file placed next to the project root (see `secrets.json.example`)

Example `secrets.json`:

```json
{
  "DISCORD_WEBHOOK_URL": "https://discord.com/api/webhooks/your_webhook_id/your_webhook_token"
}
```

Create a local secrets file from the example:

```bash
cp secrets.json.example secrets.json
# then edit secrets.json and paste your webhook URL
```

Do not commit `secrets.json`.

## Usage

Capture a single photo (and post to Discord if configured):

```bash
python3 timelapse.py
```

If you want to run without Discord, unset `DISCORD_WEBHOOK_URL` or remove/rename `secrets.json`.

To silence OpenCV/GStreamer warnings:

```bash
python3 timelapse.py 2>/dev/null
```

## Development notes

- `capture_photo(device=0, warmup_seconds=10)` will warm up the camera for the given seconds then save an image to `photos/`.
- `timelapse_lib.config.load_secrets()` prefers the environment variable and falls back to `secrets.json`.
- `timelapse_lib.discord_webhook.send_discord_message()` no-ops (with a printed warning) if no webhook is configured so you can run locally.

# Timelapse

Lightweight helper that captures a single photo from a local webcam and saves images to the `photos/` folder. Optionally posts messages (and images) to a Discord webhook.

This repository is organised as a small package so the capture logic, configuration, and Discord integration can be reused by other scripts or tests.

Contents

- `timelapse.py` — entry point that calls `timelapse_lib.cli.main()`
- `timelapse_lib/` — package with core modules (`capture.py`, `discord_webhook.py`, `config.py`, `disk_stats.py`)
- `photos/` — folder where images are saved (created automatically)
- `secrets.json.example` — example secrets file
- `requirements.txt` — Python dependencies

Requirements

- Python 3.8+
- A working webcam (e.g. `/dev/video0` on Linux)
- pip

On Debian/Ubuntu it's helpful to install `v4l-utils` and GStreamer plugins for better camera support:

```bash
sudo apt update
sudo apt install -y v4l-utils gstreamer1.0-tools gstreamer1.0-libav \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad
```

Quick install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configuration (Discord webhook)

The webhook URL is resolved in this order:

1. `DISCORD_WEBHOOK_URL` environment variable
2. `secrets.json` file placed next to the project root (see `secrets.json.example`)

Example `secrets.json`:

```json
{
  "DISCORD_WEBHOOK_URL": "https://discord.com/api/webhooks/your_webhook_id/your_webhook_token"
}
```

Create a local file from the example and edit it:

```bash
cp secrets.json.example secrets.json
# edit secrets.json and paste your webhook URL
```

Do not commit `secrets.json`.

Usage

Capture one photo and (optionally) post to Discord:

```bash
python3 timelapse.py
```

Run without Discord by unsetting `DISCORD_WEBHOOK_URL` or removing/renaming `secrets.json`.

To silence OpenCV/GStreamer warnings:

```bash
python3 timelapse.py 2>/dev/null
```

Development notes

- `timelapse_lib.capture.capture_photo(device=0, warmup_seconds=10)` warms up the camera and saves a timestamped image to `photos/`.
- `timelapse_lib.config.load_secrets()` prefers the env var and falls back to `secrets.json`.
- `timelapse_lib.discord_webhook.send_discord_message()` prints a warning and returns early if no webhook is configured (safe for local runs).

Next steps I can implement

- CLI flags (`--device`, `--warmup`, `--no-discord`) and a nicer CLI with help
- A scheduler (internal loop, cron/systemd timer) to capture on an interval and rotate old images
- Unit tests and a GitHub Actions workflow

File layout

```
timelapse.py
timelapse_lib/
photos/
secrets.json.example
requirements.txt
README.md
```

---

Tell me which follow-up you'd like and I'll implement it (CLI flags, scheduler, or tests + CI).
