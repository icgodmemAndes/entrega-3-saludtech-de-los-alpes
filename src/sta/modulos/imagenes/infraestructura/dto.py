"""DTOs para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de vuelos

"""

from sta.config.db import db

Base = db.declarative_base()


class Imagen(db.Model):
    __tablename__ = "imagenes"
    id = db.Column(db.String(40), primary_key=True)
    id_ingesta = db.Column(db.String(40), nullable=False)
    url_path = db.Column(db.String(200), nullable=False)
    estado = db.Column(db.String(40), nullable=False)
