import uuid

from sta.seedwork.aplicacion.comandos import Comando
from .base import RevertirIngestaBaseHandler
from dataclasses import dataclass
from sta.seedwork.aplicacion.comandos import ejecutar_commando as comando
from sta.modulos.ingesta.dominio.entidades import Ingesta
from sta.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from sta.modulos.ingesta.infraestructura.repositorios import RepositorioIngesta


@dataclass
class RevertirIngesta(Comando):
    id_ingesta: uuid.UUID

class RevertirIngestaHandler(RevertirIngestaBaseHandler):

    def handle(self, comando: RevertirIngesta):
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioIngesta.__class__)
        ingesta: Ingesta = repositorio.obtener_por_id(comando.id_ingesta)
        ingesta._id = comando.id_ingesta
        ingesta.revertir_ingesta()
        print(f'RRRRRRRRRR {ingesta}')

        UnidadTrabajoPuerto.registrar_batch(repositorio.revertir_entidad, ingesta)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(RevertirIngesta)
def ejecutar_comando_revertir_ingesta(comando: RevertirIngesta):
    handler = RevertirIngestaHandler()
    handler.handle(comando)
