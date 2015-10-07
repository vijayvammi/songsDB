from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import app.util as util
from math import fabs

def get_conn_string():
    params = ['conn_string', 'db_user', 
                        'db_password', 'db_server', 'db_schema']
    config_parms = util.get_config(params)
    return config_parms['conn_string'].format(**config_parms)

engine = create_engine(get_conn_string(), convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, 
                    bind=engine))
Base = declarative_base()   
def create_tables():
    # register your models here !
    #import app.model.EchoNest
    #import app.model.Word
    #import app.model.SongWords
    import app.model.Songs
    Base.metadata.create_all(bind=engine)

def get_songs(happy, excite, tempo, mode):
    from app.model.Songs import Song
    #Dynamic query for parsing mode
    if mode != -1:
        query = db_session.query(Song).filter_by(valence_label = happy, arousal_label = excite, mode = mode)
    else:
        query = db_session.query(Song).filter_by(valence_label = happy, arousal_label = excite)
    songs = query.all()
    for song in songs:
        song.tempo = round(song.tempo)
    if tempo:
        songs.sort(key=lambda song: fabs(tempo-song.tempo))
    return songs

