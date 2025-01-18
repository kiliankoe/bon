from fastapi import APIRouter
from pydantic import BaseModel
from printer import printer as p
import textwrap

router = APIRouter()

class TextRequest(BaseModel):
    title: str | None = None
    text: str

@router.post("/text")
async def text(data: TextRequest):
    """
    Print text.
    """
    if data.title:
        p.set(bold=True, double_height=True, double_width=True, underline=2)
        p.textln(data.title)
        p.set(bold=False, double_height=False, double_width=False, underline=False)
        p.ln(1)
    # TODO: Split on newlines and print each line
    p.text(textwrap.fill(data.text, width=48))
    p.cut()
    return {"message": "Printed text"}
