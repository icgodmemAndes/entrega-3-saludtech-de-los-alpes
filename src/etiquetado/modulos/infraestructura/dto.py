"""DTOs para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de vuelos

"""

from etiquetado.config.db import db, Base
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Table

import uuid




class Imagen(Base):
    __tablename__ = "imagenes"
    id = Column(String(40), primary_key=True)
    id_proveedor = Column(String(40), nullable=False)
    id_paciente = Column(String(40), nullable=False)
    url_path = Column(String(200), nullable=False)
    estado = Column(String(40), nullable=False)
