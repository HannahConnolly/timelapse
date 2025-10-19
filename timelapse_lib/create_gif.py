from datetime import datetime
from PIL import Image
import os

from timelapse_lib.config import GIFS_DIR
from timelapse_lib.config import PHOTOS_DIR


def ensure_gifs_dir():
    """
    Create a GIF from all images in the specified directory.
    
    Args:
        image_dir (str): Directory containing the image files
        output_path (str): Path where the GIF will be saved
        duration (int): Duration for each frame in milliseconds
    """
    os.makedirs(GIFS_DIR, exist_ok=True)

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