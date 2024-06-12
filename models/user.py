import secrets
import datetime
from db import Base
from passlib.context import CryptContext # type: ignore
from sqlalchemy import Column, String, Integer, DateTime # type: ignore
from sqlalchemy.sql import func

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    api_key = Column(String, index=True, unique=True, nullable=False, default=lambda: secrets.token_urlsafe(32))
    create_time = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())

    @property
    def password(self):
        raise AttributeError("Password: write-only field")

    @password.setter
    def password(self, password):
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)
