from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database.model.schema import User as UserModel
from app.helpers.hashing import Hash # Encryptar password
from app.helpers.token import create_access_token # Token


def login(db:Session, body):
  result = db.query(UserModel).filter(UserModel.username == body.username).first()
  if not result:
    return JSONResponse(content={ "message": "No se encontro el registro." }, status_code = status.HTTP_404_NOT_FOUND)
  
  if not Hash.verify(body.password, result.password):
    return JSONResponse(content={ "message": "Credenciales incorrectas." }, status_code = status.HTTP_401_UNAUTHORIZED)
  
  access_token = create_access_token(data={"sub": result.username})
  return {"access_token": access_token, "token_type": "bearer"}
  