from pydantic import BaseModel
from typing import Optional, Union

class AuthInput(BaseModel):
  username:str
  password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str ,None] = None