# Timelapse

Lightweight helper to capture photos from a local webcam, store them, and optionally post to Discord or generate AI summaries.

## Repository Contents

- `timelapse.py` — Entry point (`python3 timelapse.py`)
- `timelapse_lib/` — Core package
- `photos/` — Storage for captured images
- `.env.example` — Template for credentials
- `package.json` — Helper scripts for common tasks
- `requirements.txt` — Python dependencies

## Requirements

- Python 3.8+
- Webcam (e.g., `/dev/video0` on Linux)
- `pip`

On Linux (Debian/Ubuntu), install system dependencies for best camera support:

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

## Configuration

### Discord Webhook
Set `DISCORD_WEBHOOK_URL` in your environment or in `.env` (see `.env.example`).

### AI Features (Gemini)
To use AI summaries, set `GEMINI_API_KEY` in `.env` or your environment.

**Setup `.env`:**

```.env.example .env
# Edit .env to add your keys
```

> [!IMPORTANT]
> Do NOT commit `.env` to version control.

## Usage

### Basic Capture
Capture a single photo:

```bash
python3 timelapse.py
```

### CLI Reference
The tool supports several flags for advanced usage:

```bash
python3 -m timelapse_lib.cli [flags]
# OR via the entry point if modified to pass args (timelapse.py currently does not assume args)
# The recommended way to access full CLI features is via the library module directly:
python3 -m timelapse_lib.cli --help
```

*Note: `timelapse.py` is a simplified entry point. For full CLI features use `timelapse_lib.cli`.*

- `-h`, `--help`: Show help message
- `-a`, `--ai`: Send AI summary of the photo to the Discord AI channel
- `-d`, `--discord`: Send Discord notifications
- `-g`, `--gif`: Create an animated GIF from captured photos
- `-m`, `--gif-ms MS`: Frame duration for GIF (default: 150ms)
- `-w`, `--webm`: Create an animated WebM video
- `-f`, `--webm-fps FPS`: FPS for WebM (default: 6)

### Helper Scripts
If you have `npm` installed, you can use the predefined scripts in `package.json`:

- `npm start`: Run basic capture (`python3 timelapse.py`)
- `npm run capture`: Run via library CLI
- `npm run capture:discord`: Capture with explicit Discord flag
- `npm run capture:gif`: Create a GIF
- `npm run create:gif`: Create a GIF (alternative method)
- `npm test`: Run tests

## Development Notes

- `timelapse_lib.capture.capture_photo()` handles camera warmup and saving.
- `timelapse_lib.config` manages secrets.
- `timelapse_lib.gemini` handles interaction with Google's Gemini API.
