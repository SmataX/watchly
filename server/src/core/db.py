# src/core/db.py

from sqlmodel import SQLModel, create_engine, Session
from src.core.config import config
from typing import Annotated
from fastapi import Depends



engine = create_engine(config.DATABASE_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)