from sqlalchemy import Column, String, Integer, ForeignKey
from database import Base
from model.Word import Word

class SongWords(Base):
    __tablename__ = 'songwords'
    track_id = Column(String(100), primary_key=True) 
    word_id = Column(Integer, ForeignKey(Word.word_id), primary_key=True )
    count = Column(Integer)