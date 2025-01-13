import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

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
    difficulty: float = Field(ge=0.0, le=1.0)

@app.post("/sudoku")
async def sudoku(data: SudokuRequest):
    """
    Print a sudoku puzzle with the given difficulty.
    """
    return {"message": "Generating puzzle", "difficulty": data.difficulty}

class QRRequest(BaseModel):
    data: str

@app.post("/qr")
async def qr(data: QRRequest):
    """
    Print a QR code.
    """
    return {"message": "Generating QR code", "data": data.data}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
