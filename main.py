import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from print import daily_report, list, sudoku, furby, qr, text, image

app = FastAPI()

app.include_router(daily_report.router)
app.include_router(list.router)
app.include_router(sudoku.router)
app.include_router(furby.router)
app.include_router(qr.router)
app.include_router(text.router)
app.include_router(image.router)

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
