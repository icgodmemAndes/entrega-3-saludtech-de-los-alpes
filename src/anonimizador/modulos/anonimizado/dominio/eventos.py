from __future__ import annotations

import uuid
from dataclasses import dataclass
from anonimizador.seedwork.dominio.eventos import (EventoDominio)


@dataclass
class AnonimizadoProcesada(EventoDominio):
    id: uuid.UUID = None
    id_ingesta: uuid.UUID = None
    url_path: str = None
