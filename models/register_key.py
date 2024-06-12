from db import Base
from sqlalchemy import Column, String, Integer, DateTime # type: ignore
from sqlalchemy.sql import func # type: ignore

class RegisterKey(Base):
    __tablename__ = "register_key"

    id = Column(Integer, primary_key=True, index=True)
    register_key = Column(String, unique=True, index=True)
    create_time = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())


