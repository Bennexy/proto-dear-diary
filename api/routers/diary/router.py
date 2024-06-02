import datetime
import sys

from pydantic import BaseModel

from api.auth import validate_token
sys.path.append(".")
from fastapi import APIRouter, Depends
from uuid import UUID

from api.db.models.diary_entries import DiaryEntries, User
from api.routers.diary.models import DiaryEntryModel, DiaryEntryCreate

router = APIRouter(prefix="/diary", tags=["Diary"])




@router.get("/entries", response_model=list[DiaryEntryModel])
async def get_entries(
    user: User = Depends(validate_token)
) -> list[DiaryEntryModel]:
    return DiaryEntries.get_by_user(user)


@router.post("/create", response_model=DiaryEntryModel)
async def create_entry(
    user: User = Depends(validate_token),
    data: DiaryEntryCreate = Depends(DiaryEntryCreate)
) -> DiaryEntryModel:
    id: UUID = DiaryEntries.new(user, data)

    return DiaryEntries.get_by_id(user, id).to_model()

class Date(BaseModel):
    year: int = datetime.datetime.now().year
    month: int = datetime.datetime.now().month
    day: int = datetime.datetime.now().day

@router.get("/entries_by_date", response_model=list[DiaryEntryModel])
async def get_entries_by_date(
    user: User = Depends(validate_token),
    date: Date = Depends(Date)
) -> list[DiaryEntryModel]:
    datetime_date = datetime.date(date.year, date.month, date.day)
    return DiaryEntries.get_by_date(user, datetime_date)
