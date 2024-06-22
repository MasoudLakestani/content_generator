import configparser
from settings import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = f"postgresql://{config['database']['DB_USER']}:{config['database']['DB_PASSWORD']}@{config['database']['DB_HOST']}:{config['database']['DB_PORT']}/{config['database']['DB_NAME']}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()



ini_config = configparser.ConfigParser()

ini_config.read('alembic.ini')

ini_config['alembic']['sqlalchemy.url'] = SQLALCHEMY_DATABASE_URL

with open('alembic.ini', 'w') as configfile:
    ini_config.write(configfile)
