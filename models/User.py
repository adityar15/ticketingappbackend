from sqlalchemy import Boolean, Column, Integer, String, DateTime

from datetime import datetime

from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(32))
    role = Column(String(30))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)