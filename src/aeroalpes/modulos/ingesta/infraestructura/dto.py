"""DTOs para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de vuelos

"""

from aeroalpes.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()


class Ingesta(db.Model):
    __tablename__ = "ingestas"
    id = db.Column(db.String, primary_key=True)
    id_proveedor = db.Column(db.String, nullable=False)
    id_paciente = db.Column(db.String, nullable=False)
    url_path = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, nullable=False)

