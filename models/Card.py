from sqlalchemy import  Column, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from database import Base

class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True, index=True)
    rank = Column(Integer)
    text = Column(Text)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable = False)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    