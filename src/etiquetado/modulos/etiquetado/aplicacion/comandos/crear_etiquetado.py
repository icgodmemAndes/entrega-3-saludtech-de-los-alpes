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
    id_anonimizado: uuid.UUID
    modalidad: uuid.UUID
    region_anatomica: str
    patologia: str

class CrearEtiquetadoHandler(CrearEtiquetadoBaseHandler):

    def handle(self, comando: CrearEtiquetado):
        etiquetado_dto = EtiquetadoDTO(
            id_anonimizado=comando.id_anonimizado,
            modalidad=comando.modalidad,
            region_anatomica=comando.region_anatomica,
            patologia=comando.patologia,
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
