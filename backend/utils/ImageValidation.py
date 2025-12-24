import io

from PIL import Image

MAXSIZE = 1024 * 1024 * 5

def validate_screenshot(file: bytes):
    if len(file) > MAXSIZE:
        return ValueError("Image too large")

    image = Image.open(io.BytesIO(file))
    if image.format not in ["PNG", "JPEG"]:
        raise ValueError("Image format not supported")