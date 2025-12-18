import os
import base64
import argparse
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# Determine photos directory: CLI arg -> PHOTO_PATH env -> ./photos
parser = argparse.ArgumentParser(description="Send latest photo to Gemini")
parser.add_argument("-p", "--photos", help="Path to photos directory")
args = parser.parse_args()

default_photos_dir = Path(__file__).parent / "photos"
photos_dir = None
if args.photos:
    photos_dir = Path(args.photos).expanduser()
elif os.getenv("PHOTO_PATH"):
    photos_dir = Path(os.getenv("PHOTO_PATH") or "../photos").expanduser()
else:
    photos_dir = default_photos_dir
allowed_ext = {".jpg", ".jpeg", ".png", ".heic", ".webp"}
if not photos_dir.exists():
    raise SystemExit(f"photos directory not found: {photos_dir}")

image_files = [
    p for p in photos_dir.iterdir() if p.is_file() and p.suffix.lower() in allowed_ext
]
if not image_files:
    raise SystemExit(f"No image files found in {photos_dir}")

latest_image = max(image_files, key=lambda p: p.stat().st_mtime)

# Read and base64-encode the image
with latest_image.open("rb") as f:
    image_bytes = f.read()

prompt_text = "Respond in JSON with 'plant_score' and 'plant_care' fields. Plant score is out of 100 and give plant-care suggestions."
# Build typed content objects expected by the SDK
import mimetypes

mime_type, _ = mimetypes.guess_type(str(latest_image))
if not mime_type:
    mime_type = "image/jpeg"

text_part = types.Part.from_text(text=prompt_text)
image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
content = types.Content(parts=[text_part, image_part])

response = client.models.generate_content(
    model="gemini-2.5-flash",
    # model="gemini-2.0-flash",
    config={"response_mime_type": "application/json"},
    contents=[content],
)

print(response.text)
