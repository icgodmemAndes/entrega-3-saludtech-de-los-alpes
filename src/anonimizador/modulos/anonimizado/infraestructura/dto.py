from anonimizador.config.db import db

Base = db.declarative_base()


class Anonimizado(db.Model):
    __tablename__ = "anonimizados"
    id = db.Column(db.String(40), primary_key=True)
    id_ingesta = db.Column(db.String(40), nullable=False)
    url_path = db.Column(db.String(1000), nullable=False)
