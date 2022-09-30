from sqlalchemy import  Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from database import Base

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    title = Column(String(255))
    color = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    cards = relationship("Card", backref="category")