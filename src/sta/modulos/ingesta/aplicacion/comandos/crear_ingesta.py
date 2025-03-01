import uuid

from sta.seedwork.aplicacion.comandos import Comando
from sta.modulos.ingesta.aplicacion.dto import IngestaDTO
from .base import CrearIngestaBaseHandler
from dataclasses import dataclass
from sta.seedwork.aplicacion.comandos import ejecutar_commando as comando

from sta.modulos.ingesta.dominio.entidades import Ingesta
from sta.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from sta.modulos.ingesta.aplicacion.mapeadores import MapeadorIngesta

from sta.modulos.ingesta.infraestructura.repositorios import RepositorioIngesta
from sta.modulos.ingesta.dominio.objetos_valor import EstadoIngesta


@dataclass
class CrearIngesta(Comando):
    id_proveedor: uuid.UUID
    id_paciente: uuid.UUID
    url_path: str


class CrearIngestaHandler(CrearIngestaBaseHandler):

    def handle(self, comando: CrearIngesta):
        ingesta_dto = IngestaDTO(
            id_proveedor=comando.id_proveedor,
            id_paciente=comando.id_paciente,
            url_path=comando.url_path,
            estado=EstadoIngesta.CREADA,
        )

        ingesta: Ingesta = self.fabrica_ingesta.crear_objeto(ingesta_dto, MapeadorIngesta())
        ingesta.crear_ingesta(ingesta)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioIngesta.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, ingesta)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(CrearIngesta)
def ejecutar_comando_crear_ingesta(comando: CrearIngesta):
    handler = CrearIngestaHandler()
    handler.handle(comando)
