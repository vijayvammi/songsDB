from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import util

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
    import model.EchoNest
    Base.metadata.create_all(bind=engine)

