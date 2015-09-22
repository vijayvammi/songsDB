from sqlalchemy import Column, Integer, String, Float
from database import Base

class EchoNest(Base):
    __tablename__ = 'echonest'
    song_id = Column(String(100), primary_key=True) 
    track_id = Column(String(100))
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
    key = Column(Integer)
    mode = Column(Integer)
    time_signature = Column(Float)
