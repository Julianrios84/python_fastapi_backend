from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker
from core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
# cremos el motor
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# creamos el session pasandole el motor
session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
# crear base de datos para manejar las tablas 
base = declarative_base()


def getdb():
  db = session()
  try:
    yield db
  finally:
    db.close()