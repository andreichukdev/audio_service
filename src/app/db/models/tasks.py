from sqlalchemy import Column, Integer, String, ForeignKey, Text
from ..base import Base

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    task_name = Column(String, nullable=False)
    audio_url = Column(String, nullable=True)
    prompts = Column(Text, nullable=False)