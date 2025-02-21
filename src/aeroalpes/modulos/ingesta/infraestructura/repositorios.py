""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""

from aeroalpes.config.db import db
from aeroalpes.modulos.ingesta.dominio.entidades import Ingesta
from aeroalpes.modulos.ingesta.dominio.fabricas import FabricaIngesta
from .mapeadores import MapeadorIngesta
from aeroalpes.modulos.ingesta.dominio.repositorios import RepositorioIngesta


class RepositorioIngestaSQLite(RepositorioIngesta):

    def __init__(self):
        self._fabrica_ingesta: FabricaIngesta = FabricaIngesta()

    @property
    def fabrica_ingesta(self):
        return self._fabrica_ingesta

    def agregar(self, ingesta: Ingesta):
        ingesta_dto = self.fabrica_ingesta.crear_objeto(ingesta, MapeadorIngesta())
        db.session.add(ingesta_dto)

