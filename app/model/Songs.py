from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Song(Base):
    __tablename__ = 'songs'
    song_id = Column(String(100), primary_key=True) 
    artist = Column(String(100))
    title = Column(String(100))
    energy = Column(Float)
    liveness = Column(Float)
    tempo = Column(Float)
    speechiness = Column(Float)
    acousticness = Column(Float)
    danceability = Column(Float)
    instrumentalness = Column(Float)
    loudness = Column(Float)
    valence = Column(Float)
    key = Column(String(2))
    mode = Column(Integer)
    time_signature = Column(Float)
    valence_label = Column(Integer)
    arousal_label = Column(Integer)

    def as_dict(self): 
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}