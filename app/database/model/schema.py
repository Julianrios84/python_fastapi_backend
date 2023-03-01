from app.database.config.connect import base
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime
from sqlalchemy.schema import ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

class User(base):
  __tablename__ = "user"
  id = Column(Integer, primary_key=True, autoincrement=True)
  username = Column(String, unique=True)
  password = Column(String)
  firstname = Column(String)
  lastname = Column(String)
  address = Column(String)
  phone = Column(String)
  email = Column(String, unique=True)
  status = Column(Boolean, default=True)
  createdat = Column(DateTime, default=datetime.now(), onupdate=datetime.now)
  sale = relationship('Sale', backref='user', cascade='delete, merge')
  
class Sale(base):
  __tablename__ = "sale"
  id = Column(Integer, primary_key=True, autoincrement=True)
  userid = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"))
  sale = Column(Integer)
  sale_product = Column(Integer)