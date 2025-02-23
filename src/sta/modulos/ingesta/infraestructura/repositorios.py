""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""
from datetime import datetime
from uuid import UUID

from sta.config.db import db
from sta.modulos.ingesta.dominio.entidades import Ingesta
from sta.modulos.ingesta.dominio.fabricas import FabricaIngesta
from .mapeadores import MapeadorIngesta
from sta.modulos.ingesta.dominio.repositorios import RepositorioIngesta
from .dto import Ingesta as IngestaDTO


class RepositorioIngestaSQLite(RepositorioIngesta):

    def __init__(self):
        self._fabrica_ingesta: FabricaIngesta = FabricaIngesta()

    @property
    def fabrica_ingesta(self):
        return self._fabrica_ingesta

    def agregar(self, ingesta: Ingesta):
        ingesta.fecha_creacion = datetime.now()
        ingesta_dto = self.fabrica_ingesta.crear_objeto(ingesta, MapeadorIngesta())
        db.session.add(ingesta_dto)
        print('AGREGAR completo')

    def obtener_por_id(self, id: UUID) -> Ingesta:
        ingesta_dto = db.session.query(IngestaDTO).filter_by(id=str(id)).one()
        return self.fabrica_ingesta.crear_objeto(ingesta_dto, MapeadorIngesta())

    def obtener_todos(self) -> list[Ingesta]:
        # TODO
        raise NotImplementedError

    def actualizar(self, ingesta: Ingesta):
        # TODO
        raise NotImplementedError

    def eliminar(self, ingesta_id: UUID):
        # TODO
        raise NotImplementedError

