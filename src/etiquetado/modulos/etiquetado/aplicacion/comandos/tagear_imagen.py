import uuid

from etiquetado.seedwork.aplicacion.comandos import Comando
from etiquetado.modulos.etiquetado.aplicacion.dto import TagearDTO
from .base import TagearBaseHandler
from dataclasses import dataclass
from etiquetado.seedwork.aplicacion.comandos import ejecutar_commando as comando

from etiquetado.modulos.etiquetado.dominio.entidades import Tagear
from etiquetado.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from etiquetado.modulos.etiquetado.aplicacion.mapeadores import MapeadorTagear

from etiquetado.modulos.etiquetado.infraestructura.repositorios import RepositorioTagear



@dataclass
class Tagear(Comando):
    id_anonimizado: uuid.UUID


class TagearHandler(TagearBaseHandler):

    def handle(self, comando: Tagear):
        tagear_dto = TagearDTO(
            id_anonimizado=comando.id_anonimizado
        )

        tagear: Tagear = self.fabrica_tagear.crear_objeto(tagear_dto, MapeadorTagear())
        tagear.crear_etiquetado(tagear)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioTagear.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, tagear)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(Tagear)
def ejecutar_comando_tagear(comando: Tagear):
    handler = TagearHandler()
    handler.handle(comando)
