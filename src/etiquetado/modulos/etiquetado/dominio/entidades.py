"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de etiquetado

"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime

from etiquetado.modulos.etiquetado.dominio.eventos import EtiquetadoCreada
from etiquetado.seedwork.dominio.entidades import AgregacionRaiz, Entidad


@dataclass
class Etiquetado(AgregacionRaiz):
    id_anonimizado: uuid.UUID = field(hash=True, default=None)
    modalidad: str = field(default_factory=str)
    region_anatomica: str = field(default_factory=str)
    patologia: str = field(default_factory=str)

    def crear_etiquetado(self, etiquetado: Etiquetado):
        self.id_anonimizado = etiquetado.id_anonimizado
        self.modalidad = etiquetado.modalidad
        self.region_anatomica = etiquetado.region_anatomica
        self.patologia = etiquetado.patologia

        self.agregar_evento(
            EtiquetadoCreada(id=etiquetado.id, id_anonimizado=self.id_anonimizado, modalidad=self.modalidad,
                             region_anatomica=self.region_anatomica, patologia=self.patologia,
                             fecha_creacion=datetime.now()))
