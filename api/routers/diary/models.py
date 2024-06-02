import datetime
from uuid import UUID
from pydantic import BaseModel


class DiaryEntryModel(BaseModel):
    id: UUID
    data: str

    created_on: datetime.datetime
    modified_on: None | datetime.datetime
    deleted_on: None | datetime.datetime
    deleted: bool 


class DiaryEntryCreate(BaseModel):
    data: str