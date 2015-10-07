from sqlalchemy import Column, String, Integer
from app.database import Base

class Word(Base):
    __tablename__ = 'words'
    word_id = Column(Integer, primary_key=True)
    word = Column(String(100)) 
