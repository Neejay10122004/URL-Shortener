from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base
class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)
    clicks = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
