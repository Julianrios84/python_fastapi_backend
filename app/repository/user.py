from app.schema.user import UserCreateInput, UserUpdateInput
from app.database.model.schema import User as UserModel
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.orm import Session
# Encryptar password
from app.helpers.hashing import Hash


def getall(db:Session):
  return db.query(UserModel).all()

def create(db:Session, body: UserCreateInput):
  try:
    body.password = Hash.password(body.password)
    
    user = UserModel(**body.dict());
    db.add(user)
    db.commit()
    db.refresh(user)
    return JSONResponse(content={"message": "Registro creado correctamente." },  status_code = status.HTTP_201_CREATED)
  except Exception as e:
    return JSONResponse(content={"message": f"Error al crear el registro {e}" },  status_code = status.HTTP_409_CONFLICT)
  

def getbyid(db:Session, id: int):
  result = db.query(UserModel).filter(UserModel.id == id).first()
  if not result:
    return JSONResponse(content={ "message": "No se encontro el registro." }, status_code = status.HTTP_404_NOT_FOUND)
  return result

def delete(db:Session, id: int):
  result = db.query(UserModel).filter(UserModel.id == id).first()
  if not result:
    return JSONResponse(content={ "message": "No se encontro el registro." }, status_code = status.HTTP_404_NOT_FOUND)
  db.delete(result)
  db.commit()
  return JSONResponse(content={"message": "Registro eliminado correctamente." },  status_code = status.HTTP_200_OK)

def update(db:Session, id: int, body: UserUpdateInput):
  result = db.query(UserModel).filter(UserModel.id == id)
  if not result.first():
    return JSONResponse(content={ "message": "No se encontro el registro." }, status_code = status.HTTP_404_NOT_FOUND)
  result.update(body.dict(exclude_unset=True))
  db.commit()
  return JSONResponse(content={"message": "Registro actializado correctamente." },  status_code = status.HTTP_200_OK)