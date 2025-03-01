"""Entidades del dominio de anonimizador

En este archivo usted encontrará las entidades del dominio de anonimizador

"""

from datetime import datetime
import uuid
from anonimizador.seedwork.dominio.entidades import AgregacionRaiz
from anonimizador.modulos.dominio.eventos import ImagenProcesada
from dataclasses import dataclass, field
import anonimizador.modulos.dominio.objetos_valor as ov


@dataclass
class Imagen(AgregacionRaiz):
    id_ingesta: uuid.UUID = field(hash=True, default=None)
    url_path: str = field(default_factory=str)
    estado: ov.EstadoImagen = field(default=ov.EstadoImagen.RAW)
    fecha_anonimizacion: datetime = field(default=datetime.now())

    def crear_imagen(self, imagen):
        self.id_ingesta = imagen.id_ingesta
        self.url_path = imagen.url_path
        self.estado = imagen.estado

        self.agregar_evento(
            ImagenProcesada(id_imagen=imagen.id, id_ingesta=self.id_ingesta, url_path=self.url_path,
                            estado=self.estado))