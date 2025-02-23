"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de ingesta

"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

import sta.modulos.imagenes.dominio.objetos_valor as ov
from sta.modulos.imagenes.dominio.eventos import ImagenProcesada
from sta.seedwork.dominio.entidades import AgregacionRaiz, Entidad


@dataclass
class Imagen(AgregacionRaiz):
    id_ingesta: uuid.UUID = field(hash=True, default=None)
    url_path: str = field(default_factory=str)
    estado: ov.EstadoImagen = field(default=ov.EstadoImagen.RECHAZADA)

    def crear_imagen(self, imagen: Imagen):
        self.id_ingesta = imagen.id_ingesta
        self.url_path = imagen.url_path
        self.estado = imagen.estado

        self.agregar_evento(
            ImagenProcesada(id_imagen=imagen.id, id_ingesta=self.id_ingesta, url_path=self.url_path,
                            estado=self.estado))
