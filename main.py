import os
import random
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from escpos.printer import Usb
from sudoku import Sudoku
from draw_sudoku import draw_sudoku

p = Usb(0x04b8, 0x0e28, profile="TM-T88III")  # VendorID and ProductID, see lsusb

app = FastAPI()

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

class DailyReportRequest(BaseModel):
    todos: list[str]

@app.post("/dailyreport")
async def dailyreport(data: DailyReportRequest):
    """
    Print a daily report.
    """
    return {"message": "Generating daily report", "todos": data.todos}

class ShoppingListRequest(BaseModel):
    items: list[str]

@app.post("/shoppinglist")
async def shoppinglist(data: ShoppingListRequest):
    """
    Print a shopping list.
    """
    return {"message": "Generating shopping list", "items": data.items}

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
    p.cut()
    return {"message": "Generating puzzle", "difficulty": data.difficulty}

class QRRequest(BaseModel):
    data: str

@app.post("/qr")
async def qr(data: QRRequest):
    """
    Print a QR code.
    """
    p.qr(data.data, size=15, center=True)
    p.cut()
    return {"message": "Printed QR code", "data": data.data}

if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.178.45", port=8000, reload=True)
