import os
import datetime
import glob
import cv2
from .config import PHOTOS_DIR


def ensure_photos_dir():
    os.makedirs(PHOTOS_DIR, exist_ok=True)


def capture_photo(device=0):
    """Capture a single image from the webcam and save it under `photos/`.

    Returns the absolute path to the saved image.
    """
    ensure_photos_dir()

    # prefer v4l2 backend on linux if available
    cap = None
    try:
        if hasattr(cv2, 'CAP_V4L2'):
            cap = cv2.VideoCapture(device, cv2.CAP_V4L2)
    except Exception:
        cap = None

    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(device)

    if not cap.isOpened():
        raise RuntimeError("Could not open webcam")

    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise RuntimeError("Could not read frame from webcam")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"photo_{timestamp}.jpg"
    full_path = os.path.join(PHOTOS_DIR, filename)
    cv2.imwrite(full_path, frame)
    return os.path.abspath(full_path)


def get_latest_photo():
    patterns = [os.path.join(PHOTOS_DIR, "*.jpg"), os.path.join(PHOTOS_DIR, "*.png")]
    files = []
    for p in patterns:
        files.extend(glob.glob(p))

    if not files:
        return None
    return max(files, key=os.path.getmtime)
