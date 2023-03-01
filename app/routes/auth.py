from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.config.connect import getdb
# Repositories
from app.repository import auth as AuthRepository


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post('/login', name="Iniciar session", status_code = status.HTTP_200_OK)
def login(body: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(getdb)):
  return AuthRepository.login(db, body)