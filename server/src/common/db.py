# src/common/db.py

from sqlmodel import SQLModel, create_engine, Session
from src.common import models
from src.settings import settings
from typing import Annotated
from fastapi import Depends



engine = create_engine(settings.DATABASE_URL, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]