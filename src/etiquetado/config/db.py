from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session,Session
import os
import asyncio
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

Base = declarative_base()
engine = None
SessionLocal = None
meta = MetaData()


# Create a db object that can be imported
class Database:
    def __init__(self):
        self.session = None
    
    def get_session(self):
        if self.session is None:
            self.session = get_db_session()
        return self.session

# Instantiate the db object for importing
db = Database()

DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="127.0.0.1")
DB_PORT = os.getenv('DB_PORT', default="3306")
DB_USERNAME = os.getenv('DB_USERNAME', default="root")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="adminadmin")
DB_NAME = os.getenv('DB_NAME', default="anonimizacion")


class DatabaseConfigException(Exception):
    def __init__(self, message='Configuration file is Null or malformed'):
        self.message = message
        super().__init__(self.message)


def database_connection(config, basedir=os.path.abspath(os.path.dirname(__file__))) -> str:
    if not isinstance(config, dict):
        raise DatabaseConfigException

    if config.get('TESTING', False) == True:
        return f'sqlite:///{os.path.join(basedir, "database.db")}'
    else:
        return f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}'


async def init_db(config=None):
    """Initialize database with SQLAlchemy without Flask dependency"""
    global engine, SessionLocal
    
    if config is None:
        config = {}
    
    connection_string = database_connection(config)
    engine = create_async_engine(connection_string)
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)
    SessionLocal = Session(engine, future=True)
    #SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    
    return Session


def get_db_session():
    """Get a database session"""
    global SessionLocal
    if SessionLocal is None:
        init_db({})
    
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


async def init_engine(config=None):
    """Initialize database with SQLAlchemy without Flask dependency"""
    global engine, SessionLocal

    if config is None:
        config = {}

    connection_string = database_connection(config)
    engine = create_async_engine(connection_string)
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

    return engine

def get_db_engine():
    """Get a database session"""
    global SessionLocal
    if SessionLocal is None:
        init_engine({})

    try:
        return engine
    finally:
        print('close')