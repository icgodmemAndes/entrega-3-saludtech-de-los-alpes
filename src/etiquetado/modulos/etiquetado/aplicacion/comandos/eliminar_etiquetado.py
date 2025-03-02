import uuid

from etiquetado.seedwork.aplicacion.comandos import Comando
from .base import EliminarEtiquetadoBaseHandler
from dataclasses import dataclass
from etiquetado.seedwork.aplicacion.comandos import ejecutar_commando as comando
from etiquetado.modulos.etiquetado.dominio.entidades import Etiquetado
from etiquetado.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from etiquetado.modulos.etiquetado.infraestructura.repositorios import RepositorioEtiquetado


@dataclass
class EliminarEtiquetado(Comando):
    id_etiquetado: uuid.UUID

class EliminarEtiquetadoHandler(EliminarEtiquetadoBaseHandler):

    def handle(self, comando: EliminarEtiquetado):
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioEtiquetado.__class__)
        etiquetado: Etiquetado = repositorio.obtener_por_id(comando.id_etiquetado)
        etiquetado.eliminar_etiquetado(comando.id_etiquetado)

        UnidadTrabajoPuerto.registrar_batch(repositorio.eliminar, etiquetado.id)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(EliminarEtiquetado)
def ejecutar_comando_crear_etiquetado(comando: EliminarEtiquetado):
    handler = EliminarEtiquetadoHandler()
    handler.handle(comando)
