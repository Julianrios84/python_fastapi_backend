# Encryptar password
from passlib.context import CryptContext
pwdcontext = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
  @staticmethod
  def password(password):
    return pwdcontext.hash(password)
  
  @staticmethod
  def verify(plain, hash):
    return pwdcontext.verify(plain, hash)