from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from anonimizador.modulos.anonimizado.dominio.eventos import AnonimizadoProcesada
from anonimizador.seedwork.dominio.entidades import AgregacionRaiz, Entidad


@dataclass
class Anonimizado(AgregacionRaiz):
    id_ingesta: uuid.UUID = field(hash=True, default=None)
    url_path: str = field(default_factory=str)

    def crear_anonimizado(self, anonimizado: Anonimizado):
        self.id_ingesta = anonimizado.id_ingesta
        self.url_path = anonimizado.url_path

        self.agregar_evento(
            AnonimizadoProcesada(id=anonimizado.id, id_ingesta=self.id_ingesta, url_path=self.url_path)
        )
