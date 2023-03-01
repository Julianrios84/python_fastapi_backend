import os
from dotenv import load_dotenv
from pathlib import Path

envpath = Path('.') / '.env'
load_dotenv(dotenv_path=envpath)


class Settings:
  PROJECT_NAME:str = "PROYECTO FASTAPI"
  PROJECT_VERSION:str = "1.0"
  POSTGRES_DB:str = os.getenv('POSTGRES_DB')
  POSTGRES_USER:str = os.getenv('POSTGRES_USER')
  POSTGRES_PASSWORD:str = os.getenv('POSTGRES_PASSWORD')
  POSTGRES_HOST:str = os.getenv('POSTGRES_HOST')
  POSTGRES_PORT:str = os.getenv('POSTGRES_PORT')
  DATABASE_URL:str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
  
  TOKEN_SECRET_KEY:str = os.getenv('TOKEN_SECRET_KEY')
  TOKEN_ALGORITHM:str = os.getenv('TOKEN_ALGORITHM')
  TOKEN_ACCESS_TOKEN_EXPIRE_MINUTES:str = os.getenv('TOKEN_ACCESS_TOKEN_EXPIRE_MINUTES')
  
settings = Settings()