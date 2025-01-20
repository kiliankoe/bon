import base64
from fastapi import APIRouter, HTTPException
from printer import printer as p
from pydantic import BaseModel
from PIL import Image
import io

router = APIRouter()

class ImageRequest(BaseModel):
    """
    base64 encoded image
    """
    image: str

@router.post("/image")
async def image(data: ImageRequest):
    """
    Print an image.
    """
    try:
        image_data = base64.b64decode(data.image)
    except (base64.binascii.Error, ValueError) as e:
        raise HTTPException(status_code=400, detail=f"Invalid base64 image data: {e}")

    try:
        with Image.open(io.BytesIO(image_data)) as img:
            max_size = 740
            # TODO: Technically only the width needs to be constrained, the height can be whatever
            img.thumbnail((max_size, max_size))

            img.save("image.png", format='PNG')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process image with PIL: {e}")

    try:
        p.image("image.png")
        p.cut()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to print image: {e}")

    return {"message": "Printed image successfully"}
