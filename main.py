import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from print import daily_report, list, sudoku, furby, qr, text

app = FastAPI()

app.include_router(daily_report.router)
app.include_router(list.router)
app.include_router(sudoku.router)
app.include_router(furby.router)
app.include_router(qr.router)
app.include_router(text.router)

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.178.45", port=8000, reload=True)
