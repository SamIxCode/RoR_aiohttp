from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from settings import postgresql as settings
from sqlalchemy.orm import sessionmaker
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password_digest = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

def get_engine(user,host,port,db):
    url = f"postgresql://{user}@{host}:{port}/{db}"
    engine = create_engine(url, echo=False)
    return engine
engine = get_engine(settings['pguser'],
                settings["pghost"],
                settings["pgport"],
                settings["pgdb"])

def get_session():
    session = sessionmaker(bind=engine) ()
    return session
session = get_session()

