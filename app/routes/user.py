from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.config.connect import getdb
from app.schema.user import UserCreateInput, UserUpdateInput, UserResponseOutput
# Repositories
from app.repository import user as UserRepository
# Auth
from app.helpers.token import get_current_user

router = APIRouter(prefix="/user", tags=["Users"])

@router.get('/', name="Obtener todos los usuarios", response_model = List[UserResponseOutput], status_code = status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
def getalluser(db:Session = Depends(getdb)):
  return UserRepository.getall(db)

@router.post('/', name="Crear usuario", response_model=dict,  status_code = status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
def createuser(body: UserCreateInput, db:Session = Depends(getdb)) -> dict:
  return UserRepository.create(db, body)
 

@router.get('/{id}', name="Obtener un usuario por id", response_model=UserResponseOutput, status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
def getbyiduser(id: int, db:Session = Depends(getdb)) -> UserResponseOutput:
  return UserRepository.getbyid(db, id);
  
    
@router.delete('/{id}', name="Eliminar un usuario por id", status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
def deleteuser(id: int, db:Session = Depends(getdb)) -> dict:
  return UserRepository.delete(db, id)
  

@router.put('/{id}', name="Actualizar un usuario", status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
def updateuser(id: int, body: UserUpdateInput, db:Session = Depends(getdb)) -> dict:
  return UserRepository.update(db, id, body)