import uuid

from etiquetado.seedwork.aplicacion.comandos import Comando
from etiquetado.modulos.etiquetado.aplicacion.dto import RevertirDTO
from .base import RevertirEtiquetadoBaseHandler
from dataclasses import dataclass
from etiquetado.seedwork.aplicacion.comandos import ejecutar_commando as comando

from etiquetado.modulos.etiquetado.dominio.entidades import Revertir
from etiquetado.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from etiquetado.modulos.etiquetado.aplicacion.mapeadores import MapeadorRevertir

from etiquetado.modulos.etiquetado.infraestructura.repositorios import RepositorioEtiquetado
from etiquetado.modulos.etiquetado.dominio.objetos_valor import EstadoEtiquetado


@dataclass
class RevertirEtiquetado(Comando):
    id_anonimizado: uuid.UUID
    modalidad: uuid.UUID
    region_anatomica: str
    patologia: str

class RevertirEtiquetadoHandler(RevertirEtiquetadoBaseHandler):

    def handle(self, comando: RevertirEtiquetado):
        revertir_dto = RevertirDTO(
            id_anonimizado=comando.id_anonimizado,
            modalidad=comando.modalidad,
            region_anatomica=comando.region_anatomica,
            patologia=comando.patologia,
            estado=EstadoEtiquetado.RECHAZADO,
        )

        revertir: Revertir = self.fabrica_etiquetado.crear_objeto(revertir_dto, MapeadorRevertir())
        revertir.revertir_etiquetado(revertir)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioEtiquetado.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, revertir)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(RevertirEtiquetado)
def ejecutar_comando_revertir_etiquetado(comando: RevertirEtiquetado):
    handler = RevertirEtiquetadoHandler()
    handler.handle(comando)
