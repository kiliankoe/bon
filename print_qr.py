from fastapi import APIRouter
from pydantic import BaseModel
from printer import printer as p

router = APIRouter()

class QRRequest(BaseModel):
    data: str
    size: int = 15

@router.post("/qr")
async def qr(data: QRRequest):
    """
    Print a QR code.
    """
    p.qr(data.data, size=data.size, center=True)
    p.cut()
    return {"message": "Printed QR code"}
