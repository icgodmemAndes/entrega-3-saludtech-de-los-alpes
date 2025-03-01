import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="127.0.0.1")
DB_PORT = os.getenv('DB_PORT', default="3306")
DB_USERNAME = os.getenv('DB_USERNAME', default="root")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="adminadmin")
DB_NAME = os.getenv('DB_NAME', default="anonimizaciones")

SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()