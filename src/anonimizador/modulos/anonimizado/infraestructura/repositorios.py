from uuid import UUID
from datetime import datetime

from anonimizador.config.db import db
from anonimizador.modulos.anonimizado.dominio.entidades import Anonimizado, EstadoAnonimizado
from anonimizador.modulos.anonimizado.dominio.fabricas import FabricaAnonimizado
from .mapeadores import MapeadorAnonimizado, revertir_base64
from anonimizador.modulos.anonimizado.dominio.repositorios import RepositorioAnonimizado
from .dto import Anonimizado as AnonimizadoDTO


class RepositorioAnonimizadoSQLite(RepositorioAnonimizado):

    def __init__(self):
        self._fabrica_anonimizado: FabricaAnonimizado = FabricaAnonimizado()

    @property
    def fabrica_anonimizado(self):
        return self._fabrica_anonimizado

    def agregar(self, anonimizado: Anonimizado):
        anonimizado.fecha_creacion = datetime.now()
        anonimizado_dto = self.fabrica_anonimizado.crear_objeto(anonimizado, MapeadorAnonimizado())
        db.session.add(anonimizado_dto)

    def obtener_por_id(self, id: UUID) -> Anonimizado:
        anonimizado_dto = db.session.query(AnonimizadoDTO).filter_by(id=str(id)).one()
        return self.fabrica_anonimizado.crear_objeto(anonimizado_dto, MapeadorAnonimizado())

    def obtener_todos(self) -> list[Anonimizado]:
        # TODO
        raise NotImplementedError

    def actualizar(self, anonimizado: Anonimizado):
        # TODO
        raise NotImplementedError

    def eliminar(self, anonimizado_id: UUID):
        # TODO
        raise NotImplementedError
    
    def revertir_anonimizado(self, anonimizado: Anonimizado):
        anonimizado = db.session.query(AnonimizadoDTO).filter_by(id=str(anonimizado.id)).one()

        anonimizado.estado = EstadoAnonimizado.REVERTIDA
        anonimizado.url_path = 'revertida'
       
