from fastapi import APIRouter
from pydantic import BaseModel
from printer import printer as p
import textwrap

router = APIRouter()

class ListRequest(BaseModel):
    title: str = "Einkaufsliste"
    items: list[str]
    item_prefix: str = "  - "
    note: str | None = None

# todo_prefix = " [ ] "
# shopping_prefix = "  - "

@router.post("/list")
async def list(data: ListRequest):
    """
    Print a list of items.
    """
    p.set(align="center", font="b", bold=True, width=3, height=3, custom_size=True)
    p.textln(data.title)
    p.ln(2)
    p.set(align="left", font="b", bold=False, width=2, height=2, custom_size=True)
    for item in data.items:
        p.textln(textwrap.fill(f"{data.item_prefix}{item}", width=48))
        p.ln(1)
    if data.note:
        p.ln(2)
        p.set(align="center", font="b", bold=True, width=2, height=2, custom_size=True)
        p.textln(textwrap.fill(f"{data.note}", width=48))
    p.ln(5)
    p.cut()
    return {"message": "Printed list"}
