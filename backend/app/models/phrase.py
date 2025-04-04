from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func

from app.db.base import Base

class Phrase(Base):
    __tablename__ = "phrases"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    hash_url = Column(String, unique=True, index=True, nullable=False)
    location_name = Column(String, nullable=True)
    location_x = Column(Integer, nullable=True)
    location_y = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 