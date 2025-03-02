import uuid

from sta.seedwork.aplicacion.comandos import Comando
from .base import EliminarIngestaBaseHandler
from dataclasses import dataclass
from sta.seedwork.aplicacion.comandos import ejecutar_commando as comando
from sta.modulos.ingesta.dominio.entidades import Ingesta
from sta.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from sta.modulos.ingesta.infraestructura.repositorios import RepositorioIngesta


@dataclass
class EliminarIngesta(Comando):
    id_ingesta: uuid.UUID

class EliminarIngestaHandler(EliminarIngestaBaseHandler):

    def handle(self, comando: EliminarIngesta):
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioIngesta.__class__)
        ingesta: Ingesta = repositorio.obtener_por_id(comando.id_ingesta)
        ingesta.eliminar_ingesta()

        UnidadTrabajoPuerto.registrar_batch(repositorio.eliminar, comando.id_ingesta)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(EliminarIngesta)
def ejecutar_comando_eliminar_ingesta(comando: EliminarIngesta):
    handler = EliminarIngestaHandler()
    handler.handle(comando)
