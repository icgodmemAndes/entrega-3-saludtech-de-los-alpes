"""Entidades del dominio de anonimizador

En este archivo usted encontrará las entidades del dominio de anonimizador

"""

from datetime import datetime
import uuid
from anonimizador.seedwork.dominio.entidades import AgregacionRaiz
from anonimizador.modulos.dominio.eventos import IngestaProcesada
from dataclasses import dataclass, field
import anonimizador.modulos.dominio.objetos_valor as ov


@dataclass
class Ingesta(AgregacionRaiz):
    id_proveedor : str = field(default_factory=str)
    id_paciente : str = field(default_factory=str)
    id_ingesta: uuid.UUID = field(hash=True, default=None)
    url_path: str = field(default_factory=str)
    estado: ov.EstadoIngesta = field(default=ov.EstadoIngesta.RAW)
    fecha_anonimizacion: datetime = field(default=datetime.now())

    def crear_imagen(self, imagen):
        self.id_ingesta = imagen.id_ingesta
        self.url_path = imagen.url_path
        self.estado = imagen.estado

        #self.agregar_evento(
            #IngestaProcesada(id_imagen=imagen.id, id_ingesta=self.id_ingesta, url_path=self.url_path,
                            #estado=self.estado))