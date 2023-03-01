from pydantic import BaseModel
from typing import Optional

class UserCreateInput(BaseModel):
  username: str
  password: str
  firstname: str
  lastname: str
  address: Optional[str]
  phone: str
  email: str
 
class UserUpdateInput(BaseModel):
  username: Optional[str]
  password: Optional[str]
  firstname: Optional[str]
  lastname: Optional[str]
  address: Optional[str]
  phone: Optional[str]
  email: Optional[str]
  
class UserResponseOutput(BaseModel):
  username: str
  firstname: str
  lastname: str
  email: str
  class Config:
    orm_mode = True
  
  
  
