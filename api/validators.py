from fastapi import UploadFile, HTTPException
from PIL import Image

MAX_FILE_SIZE = 5*1024*1024  # 5mb
MAX_IMAGE_WIDTH = 4096
MAX_IMAGE_HEIGHT = 4096

ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp"
}


def validate_image(file: UploadFile):

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds 5 MB limit"
        )

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    try:
        image = Image.open(file.file)
        image.load()

        width, height = image.size

        if width > MAX_IMAGE_WIDTH or height > MAX_IMAGE_HEIGHT:
            raise HTTPException(
                status_code=400,
                detail="Image dimensions exceed the allowed limit"
            )

        image = image.convert("RGB")

    except OSError:
        raise HTTPException(
            status_code=400,
            detail="Invalid image file"
        )

    return image
