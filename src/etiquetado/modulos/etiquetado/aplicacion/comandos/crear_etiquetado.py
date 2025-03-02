import uuid

from etiquetado.seedwork.aplicacion.comandos import Comando
from etiquetado.modulos.etiquetado.aplicacion.dto import EtiquetadoDTO
from .base import CrearEtiquetadoBaseHandler
from dataclasses import dataclass
from etiquetado.seedwork.aplicacion.comandos import ejecutar_commando as comando

from etiquetado.modulos.etiquetado.dominio.entidades import Etiquetado
from etiquetado.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from etiquetado.modulos.etiquetado.aplicacion.mapeadores import MapeadorEtiquetado

from etiquetado.modulos.etiquetado.infraestructura.repositorios import RepositorioEtiquetado
from etiquetado.modulos.etiquetado.dominio.objetos_valor import EstadoEtiquetado


@dataclass
class CrearEtiquetado(Comando):
    id_proveedor: uuid.UUID
    id_paciente: uuid.UUID
    url_path: str


class CrearEtiquetadoHandler(CrearEtiquetadoBaseHandler):

    def handle(self, comando: CrearEtiquetado):
        etiquetado_dto = EtiquetadoDTO(
            id_proveedor=comando.id_proveedor,
            id_paciente=comando.id_paciente,
            url_path=comando.url_path,
            estado=EstadoEtiquetado.CREADA,
        )

        etiquetado: Etiquetado = self.fabrica_etiquetado.crear_objeto(etiquetado_dto, MapeadorEtiquetado())
        etiquetado.crear_etiquetado(etiquetado)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioEtiquetado.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, etiquetado)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(CrearEtiquetado)
def ejecutar_comando_crear_etiquetado(comando: CrearEtiquetado):
    handler = CrearEtiquetadoHandler()
    handler.handle(comando)
