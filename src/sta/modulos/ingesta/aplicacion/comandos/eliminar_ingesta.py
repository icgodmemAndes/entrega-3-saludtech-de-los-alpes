import uuid

from sta.seedwork.aplicacion.comandos import Comando
from sta.modulos.ingesta.aplicacion.dto import EliminarIngestaDTO
from .base import CrearIngestaBaseHandler, EliminarIngestaBaseHandler
from dataclasses import dataclass
from sta.seedwork.aplicacion.comandos import ejecutar_commando as comando

from sta.modulos.ingesta.dominio.entidades import Ingesta
from sta.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from sta.modulos.ingesta.aplicacion.mapeadores import MapeadorIngesta

from sta.modulos.ingesta.infraestructura.repositorios import RepositorioIngesta
from sta.modulos.ingesta.dominio.objetos_valor import EstadoIngesta


@dataclass
class EliminarIngesta(Comando):
    id_ingesta: uuid.UUID

class EliminarIngestaHandler(EliminarIngestaBaseHandler):

    def handle(self, comando: EliminarIngesta):
        ingesta_dto = EliminarIngestaDTO(
            id_ingesta=comando.id_ingesta,
            estado=EstadoIngesta.ELIMINADA,
        )

        ingesta: Ingesta = self.fabrica_ingesta.crear_objeto(ingesta_dto, MapeadorIngesta())
        ingesta.eliminar_ingesta(ingesta)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioIngesta.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.eliminar, ingesta.id)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(EliminarIngesta)
def ejecutar_comando_crear_ingesta(comando: EliminarIngesta):
    handler = EliminarIngestaHandler()
    handler.handle(comando)
