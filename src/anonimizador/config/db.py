import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

DB_HOSTNAME = os.getenv('DB_HOSTNAME', "127.0.0.1")
DB_PORT = os.getenv('DB_PORT', "3306")
DB_USERNAME = os.getenv('DB_USERNAME', "root")
DB_PASSWORD = os.getenv('DB_PASSWORD', "adminadmin")
DB_NAME_ANONIMIZACION = os.getenv('DB_NAME_ANONIMIZACION', "ingestas")


url = URL.create(
    drivername="mysql+pymysql",
    host=DB_HOSTNAME,
    port=DB_PORT,
    username=DB_USERNAME,
    password=DB_PASSWORD,
    database=DB_NAME_ANONIMIZACION
)
engine = create_engine(url)
Session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
session = Session()



