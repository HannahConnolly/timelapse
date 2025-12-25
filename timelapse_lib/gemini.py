import os
import base64
import dotenv
from pathlib import Path
from google import genai
from google.genai import types
import json
from .database import store_photo, store_analysis, extract_plant_score

def send_to_gemini():
    dotenv.load_dotenv()
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    default_photos_dir = Path(__file__).parent.parent / "photos"
    photos_dir = None
    if os.getenv("PHOTO_PATH"):
        photos_dir = Path(os.getenv("PHOTO_PATH") or "./photos").expanduser()
    else:
        photos_dir = default_photos_dir

    # If the configured path is relative (e.g. "photos" or "./photos"),
    # interpret it relative to the project root so cron (or other CWDs)
    # still find the correct directory.
    if not photos_dir.is_absolute():
        photos_dir = (Path(__file__).parent.parent / photos_dir).resolve()
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

    response_text = response.text

    # Try to parse structured JSON response
    plant_score = None
    description = None
    try:
        parsed = json.loads(response_text)
        plant_score = parsed.get("plant_score")
        description = parsed.get("plant_care") or parsed.get("plant_care_suggestions") or parsed.get("description")
    except Exception:
        parsed = None

    # Fallback: attempt to extract a numeric score from free-text
    if plant_score is None:
        try:
            plant_score = extract_plant_score(response_text)
        except Exception:
            plant_score = None

    # Fallback description
    if not description:
        description = response_text

    # Ensure the photo is recorded in the DB and store the AI analysis
    try:
        photo_id = store_photo(latest_image)
    except Exception:
        photo_id = None

    try:
        if photo_id is not None:
            store_analysis(photo_id, description, plant_score=plant_score)
    except Exception:
        pass

    return response_text
