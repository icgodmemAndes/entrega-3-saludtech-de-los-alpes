"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de etiquetado

"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

import etiquetado.modulos.imagenes.dominio.objetos_valor as ov
from etiquetado.modulos.imagenes.dominio.eventos import ImagenProcesada
from etiquetado.seedwork.dominio.entidades import AgregacionRaiz, Entidad


@dataclass
class Imagen(AgregacionRaiz):
    id_etiquetado: uuid.UUID = field(hash=True, default=None)
    url_path: str = field(default_factory=str)
    estado: ov.EstadoImagen = field(default=ov.EstadoImagen.RECHAZADA)

    def crear_imagen(self, imagen: Imagen):
        self.id_etiquetado = imagen.id_etiquetado
        self.url_path = imagen.url_path
        self.estado = imagen.estado

        self.agregar_evento(
            ImagenProcesada(id_imagen=imagen.id, id_etiquetado=self.id_etiquetado, url_path=self.url_path,
                            estado=self.estado))
