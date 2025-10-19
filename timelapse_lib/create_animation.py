from datetime import datetime
from PIL import Image
import os
import cv2
import numpy as np

from timelapse_lib.config import GIFS_DIR
from timelapse_lib.config import PHOTOS_DIR

# Create videos directory next to GIFS_DIR
VIDEOS_DIR = os.path.join(os.path.dirname(GIFS_DIR), "videos")


def ensure_gifs_dir():
    """
    Create a GIF from all images in the specified directory.
    
    Args:
        image_dir (str): Directory containing the image files
        output_path (str): Path where the GIF will be saved
        duration (int): Duration for each frame in milliseconds
    """
    os.makedirs(GIFS_DIR, exist_ok=True)

def ensure_videos_dir():
    """Create the videos directory if it doesn't exist."""
    os.makedirs(VIDEOS_DIR, exist_ok=True)

def create_webm(fps=30):
    """
    Create a WebM video from all images in the specified directory.
    
    Args:
        fps (int): Frames per second for the output video
    """
    ensure_videos_dir()

    # Ensure the photos directory exists
    if not os.path.exists(PHOTOS_DIR):
        raise ValueError(f"Photos directory does not exist: {PHOTOS_DIR}")
    
    # Get all image files in the directory
    image_files = []
    for filename in sorted(os.listdir(PHOTOS_DIR)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(PHOTOS_DIR, filename)
            image_files.append(file_path)
    
    if not image_files:
        raise ValueError(f"No images found in the directory: {PHOTOS_DIR}")
    
    # Read first image to get dimensions
    first_image = cv2.imread(image_files[0])
    height, width = first_image.shape[:2]
    
    # Create output path
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"timelapse_{timestamp}.webm"
    output_path = os.path.join(VIDEOS_DIR, filename)
    
    # Try multiple codecs and pick the first that works. OpenCV/ffmpeg builds
    # vary in which codecs are available. We'll attempt common candidates
    # and return the first successful VideoWriter.
    candidates = [
        ('VP90', "VP9 (webm, libvpx-vp9)"),
        ('VP80', "VP8 (webm, libvpx)"),
        ('X264', "H.264 (mp4)") ,
        ('avc1', "H.264 (alternate)"),
        ('MP4V', "MPEG-4"),
        ('MJPG', "Motion JPEG")
    ]

    out = None
    used_codec = None
    for code, human in candidates:
        fourcc = cv2.VideoWriter_fourcc(*code)
        writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        # Test if writer was opened successfully
        if writer.isOpened():
            out = writer
            used_codec = (code, human)
            break
        else:
            # release if partially created
            try:
                writer.release()
            except Exception:
                pass

    if out is None:
        # Provide actionable fallback instructions using ffmpeg
        raise RuntimeError(
            "Unable to create VideoWriter with available codecs. "
            "Your OpenCV build may lack WebM/VP8/VP9 support. "
            "You can create a WebM with ffmpeg as a fallback. Example:\n\n"
            "ffmpeg -framerate 30 -pattern_type glob -i 'photos/*.jpg' "
            "-c:v libvpx -b:v 1M output.webm\n\n"
            "or for VP9 (better quality, slower):\n"
            "ffmpeg -framerate 30 -pattern_type glob -i 'photos/*.jpg' "
            "-c:v libvpx-vp9 -b:v 0 -crf 30 output.webm"
        )
    
    try:
        print(f"Using codec: {used_codec[0]} ({used_codec[1]})")
        # Write each frame to video
        for image_path in image_files:
            frame = cv2.imread(image_path)
            if frame is not None:
                out.write(frame)
    finally:
        # Make sure to release the VideoWriter
        out.release()
    
    print(f"Created WebM video: {output_path}")
    return output_path

def create_gif(gif_ms=150):
    ensure_gifs_dir()  # Ensure the output directory exists

    # Ensure the photos directory exists
    if not os.path.exists(PHOTOS_DIR):
        raise ValueError(f"Photos directory does not exist: {PHOTOS_DIR}")
        
    # Get all image files in the directory
    images = []
    print("PHOTOS_DIR:", PHOTOS_DIR)
    for filename in sorted(os.listdir(PHOTOS_DIR)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(PHOTOS_DIR, filename)
            images.append(Image.open(file_path))
    
    if not images:
        raise ValueError(f"No images found in the directory: {PHOTOS_DIR}")
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"gif_{timestamp}.gif"
    output_path = os.path.join(GIFS_DIR, filename)
    
    # Save the GIF with enhanced quality settings
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        duration=gif_ms,
        loop=0,
        optimize=False,  # Disable optimization to preserve quality
        quality=100,     # Use maximum quality
        colors=256,      # Use maximum color palette
        dither=Image.Dither.FLOYDSTEINBERG  # Use high quality dithering
    )

    full_path = os.path.join(GIFS_DIR, filename)
    print(full_path)
    return os.path.abspath(full_path)

if __name__ == "__main__":
    create_gif()