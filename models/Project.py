from sqlalchemy import  Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from database import Base

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    categories = relationship("Category", backref="project")