import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from print_daily_report import router as daily_report_router
from print_list import router as list_router
from print_sudoku import router as sudoku_router
from print_furby import router as furby_router
from print_qr import router as qr_router
from print_text import router as text_router

app = FastAPI()

app.include_router(daily_report_router)
app.include_router(list_router)
app.include_router(sudoku_router)
app.include_router(furby_router)
app.include_router(qr_router)
app.include_router(text_router)

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.178.45", port=8000, reload=True)
