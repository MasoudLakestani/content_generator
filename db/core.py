from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import config


SQLALCHEMY_DATABASE_URL = f"postgresql://{config['database']['DB_USER']}:{config['database']['DB_PASSWORD']}@{config['database']['DB_HOST']}:{config['database']['DB_PORT']}/{config['database']['DB_NAME']}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
