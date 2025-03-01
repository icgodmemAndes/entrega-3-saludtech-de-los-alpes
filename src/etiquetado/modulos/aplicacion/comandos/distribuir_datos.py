import uuid

from etiquetado.seedwork.aplicacion.comandos import Comando, ComandoHandler
from etiquetado.seedwork.aplicacion.comandos import ejecutar_commando as comando
from etiquetado.modulos.dominio.entidades import Dato
from etiquetado.modulos.dominio.objetos_valor import EstadoEtiquetado
from dataclasses import dataclass
import datetime
import time



@dataclass
class ComandoDistribuirDatos(Comando):
    id_proveedor: uuid.UUID
    id_paciente: uuid.UUID
    url_path: str
    estado: str
    etiquetas: list[str]
    modelo_utilizado: str
    confianza: float

class DistribuirDatosHandler(ComandoHandler):

    def a_entidad(self, comando: ComandoDistribuirDatos) -> Dato:

        dato = Dato(
            id_proveedor=comando.id_proveedor,
            id_paciente=comando.id_paciente,
            url_path=comando.url_path,
            estado=EstadoEtiquetado.FINALIZADA,
            etiquetas=comando.etiquetas,
            modelo_utilizado=comando.modelo_utilizado,
            confianza=comando.confianza
        )
        return dato

    def handle(self, comando: ComandoDistribuirDatos):

        dato = self.a_entidad(comando)


@comando.register(ComandoDistribuirDatos)
def ejecutar_comando_distribuir_datos(comando: ComandoDistribuirDatos):
    handler = DistribuirDatosHandler()
    handler.handle(comando)