from anonimizador.config.db import db

import uuid

Base = db.declarative_base()


class Imagen(db.Model):
    __tablename__ = "imagenes"
    id = db.Column(db.String(40), primary_key=True)
    id_ingesta = db.Column(db.String(40), nullable=False)
    url_path = db.Column(db.String(200), nullable=False)
    estado = db.Column(db.String(40), nullable=False)
