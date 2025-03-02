# dto.py (or wherever your model classes reside)
from sqlalchemy import Column, String, Integer
from anonimizador.config.db import Base

class Imagen(Base):
    __tablename__ = "ingestas_anonimizadas"

    id = Column(String(40), primary_key=True)
    id_ingesta = Column(String(40), nullable=False)
    url_path = Column(String(200), nullable=False)
    estado = Column(String(40), nullable=False)