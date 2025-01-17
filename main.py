import os
import random
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from escpos.printer import Usb
from sudoku import Sudoku
from draw_sudoku import draw_sudoku
import textwrap

from util import cat_announcement

# TODO: Read VendorID and ProductID from `lsusb` output on startup
p = Usb(0x04b8, 0x0e28, profile="TM-T88III")

app = FastAPI()

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

class DailyReportRequest(BaseModel):
    todos: list[str]

@app.post("/daily")
async def daily(data: DailyReportRequest):
    """
    Print a daily report.
    """
    cat_announcement(p)
    p.textln("Daily Report")
    p.ln(2)
    p.cut()
    return {"message": "Generating daily report", "todos": data.todos}

class ShoppingRequest(BaseModel):
    items: list[str]

@app.post("/shopping")
async def shopping(data: ShoppingRequest):
    """
    Print a shopping list.
    """
    p.set(align="center", font="b", bold=True, width=3, height=3, custom_size=True)
    p.textln("Einkaufsliste")
    p.ln(2)
    p.set(align="left", font="b", bold=False, width=2, height=2, custom_size=True)
    for item in data.items:
        p.textln(f"  - {item}")
        p.ln(1)
    p.ln(5)
    p.cut()
    return {"message": "Generating shopping list", "items": data.items}

class TodoRequest(BaseModel):
    title: str = "ToDo"
    todos: list[str]

@app.post("/todo")
async def todo(data: TodoRequest):
    """
    Print a todo list.
    """
    p.set(align="center", font="b", bold=True, width=3, height=3, custom_size=True)
    p.textln(data.title)
    p.ln(2)
    p.set(align="left", font="b", bold=False, width=2, height=2, custom_size=True)
    for item in data.todos:
        p.textln(f" [ ] {item}")
        p.ln(1)
    p.ln(5)
    p.cut()
    return {"message": "Generating todo list", "todos": data.todos}

class SudokuRequest(BaseModel):
    difficulty: float = Field(0.4, ge=0.0, le=1.0)

@app.post("/sudoku")
async def sudoku(data: SudokuRequest):
    """
    Print a sudoku puzzle with the given difficulty.
    """
    puzzle = Sudoku(3, seed=random.randint(0, 1000000)).difficulty(data.difficulty)
    if os.path.exists("sudoku.png"):
        os.remove("sudoku.png")
    draw_sudoku(puzzle.board)
    p.image("sudoku.png")
    p.ln(2)
    p.cut()
    return {"message": "Generating puzzle", "difficulty": data.difficulty}

@app.post("/furby")
async def furby():
    """
    Print a furby.
    """
    p.image("furby.png")
    p.cut()
    return {"message": "Generating furby", "cuteness": 1}

class QRRequest(BaseModel):
    data: str
    size: int = 15

@app.post("/qr")
async def qr(data: QRRequest):
    """
    Print a QR code.
    """
    p.qr(data.data, size=data.size, center=True)
    p.cut()
    return {"message": "Printed QR code", "data": data.data}

class TextRequest(BaseModel):
    title: str | None = None
    text: str

@app.post("/text")
async def text(data: TextRequest):
    """
    Print text.
    """
    if data.title:
        p.set(bold=True, double_height=True, double_width=True, underline=2)
        p.textln(data.title)
        p.set(bold=False, double_height=False, double_width=False, underline=False)
        p.ln(1)
    p.text(textwrap.fill(data.text, width=48))
    p.cut()
    return {"message": "Printed text", "title": data.title, "text": data.text}

if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.178.45", port=8000, reload=True)
