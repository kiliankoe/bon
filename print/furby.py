from fastapi import APIRouter
from printer import printer as p

router = APIRouter()

@router.post("/furby")
async def furby():
    """
    Print a furby.
    """
    p.image("furby.png")
    p.cut()
    return {"message": "Printed furby"}
