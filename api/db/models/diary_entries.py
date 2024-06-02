import datetime
import sys

import uuid
from sqlalchemy import Column, Date, ForeignKey, UUID, Text, DateTime, Boolean, func

from api.db.models.users import User
from api.exceptions.db import DiaryServerDBException
from api.routers.diary.models import DiaryEntryCreate, DiaryEntryModel

sys.path.append(".")
from api.db.database import db, DB, Base




class DiaryEntries(Base):
    __tablename__ = "dieary_entries"

    id: Column[UUID] = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False, unique=True, default=uuid.uuid4())
    user: Column[UUID] = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    entry: Column[Text] = Column(Text())
    
    
    created_on: Column[DateTime] = Column(DateTime(), nullable=False, server_default=func.now())
    last_modified_on: Column[DateTime] = Column(DateTime(), nullable=True, onupdate=func.now())
    deleted_on: Column[DateTime] = Column(DateTime(), nullable=True)
    deleted: Column[Boolean] = Column(Boolean(), nullable=False, default=False)
    

    @db
    def new(user: User, data: DiaryEntryCreate, db: DB) -> "UUID":
        diary_entries = DiaryEntries()

        diary_entries.id = uuid.uuid4()
        diary_entries.user = user.id
        diary_entries.entry = data.data


        db.add(diary_entries)
        db.commit()

        return diary_entries.id

    @db
    def update(self, data: str, db: DB) -> "DiaryEntries":
        self.entry = data

        db.add(self)
        db.commit()

        return self
    
    @db
    @staticmethod
    def get_by_user(user: User, db: DB) -> list["DiaryEntryModel"]:
        
        entries: list[DiaryEntryModel] = []
        for entry in db.query(DiaryEntries).filter(DiaryEntries.user == user.id).all():
            entries.append(entry.to_model())

        return entries
    
    @db
    @staticmethod
    def get_all(db: DB) -> list["DiaryEntryModel"]:
        
        entries: list[DiaryEntryModel] = []
        for entry in db.query(DiaryEntries).all():
            entries.append(entry.to_model())

        return entries

    @db
    @staticmethod
    def get_by_id(user: User, id: UUID, db: DB) -> DiaryEntryModel:
        entry: DiaryEntries | None = db.query(DiaryEntries).filter(DiaryEntries.user == user.id, DiaryEntries.id == id).first()

        if entry is None:
            raise DiaryServerDBException(
                'No diary entry found with the id', {}, User
            )
        
        return entry

    @db
    @staticmethod
    def get_by_date(user: User, date: datetime.date, db: DB) -> list[DiaryEntryModel]:
        results: list[DiaryEntries] = db.query(
            DiaryEntries
        ).filter(
            DiaryEntries.user == user.id, 
            DiaryEntries.created_on >= datetime.datetime.combine(date, datetime.datetime.min.time()),
            DiaryEntries.created_on <= datetime.datetime.combine(date, datetime.datetime.max.time())
        ).all()

        entries = []
        for entry in results:
            entries.append(entry.to_model())

        return entries

    def to_model(self) -> DiaryEntryModel:
        model = DiaryEntryModel(
            id = self.id,
            created_on = self.created_on,
            data = self.entry,
            deleted = self.deleted,
            deleted_on = self.deleted_on,
            modified_on = self.last_modified_on,
        )

        return model
