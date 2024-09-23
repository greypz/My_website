#  put here the converted code from django to sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship,declarative_base
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .Base import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True,index=True)
    username = Column(String, unique=True)
    email=Column(String,unique=True )
    password = Column(String)
    phone = Column(String)
    role = Column(String, default="user")
    messages = relationship("Message", back_populates="user")

    def __repr__(self):
        return f"<User(username={self.username}, phone={self.phone})>"