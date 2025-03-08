import uuid

from sta.seedwork.aplicacion.comandos import Comando
from sta.modulos.ingesta.aplicacion.dto import IngestaDTO
from .base import AlertaIngestaBaseHandler
from dataclasses import dataclass
from sta.seedwork.aplicacion.comandos import ejecutar_commando as comando

from sta.modulos.ingesta.dominio.entidades import Ingesta
from sta.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from sta.modulos.ingesta.aplicacion.mapeadores import MapeadorIngesta

from sta.modulos.ingesta.infraestructura.repositorios import RepositorioIngesta
from sta.modulos.ingesta.dominio.objetos_valor import EstadoIngesta


@dataclass
class AlertaIngesta(Comando):
    id_ingesta: uuid.UUID


class AlertaIngestaHandler(AlertaIngestaBaseHandler):

    def handle(self, comando: AlertaIngesta):
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioIngesta.__class__)
        ingesta: Ingesta = repositorio.obtener_por_id(comando.id_ingesta)

        ingesta.alerta_ingesta()

        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(AlertaIngesta)
def ejecutar_comando_alerta_ingesta(comando: AlertaIngesta):
    handler = AlertaIngestaHandler()
    handler.handle(comando)
