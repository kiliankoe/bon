from fastapi import APIRouter
from pydantic import BaseModel
from util import cat_announcement
from printer import printer as p

router = APIRouter()

class DailyReportRequest(BaseModel):
    todos: list[str]

@router.post("/daily")
async def daily(data: DailyReportRequest):
    """
    Print a daily report.
    """
    cat_announcement(p)
    p.textln("Daily Report")
    p.ln(2)
    p.cut()
    return {"message": "Printed daily report"}
