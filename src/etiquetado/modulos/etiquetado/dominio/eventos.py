from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from etiquetado.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime


@dataclass
class EtiquetadoCreada(EventoDominio):
    id: uuid.UUID = None
    id_anonimizado: uuid.UUID = None
    modalidad: uuid.UUID = None
    region_anatomica: str = None
    patologia: str = None
    fecha_creacion: datetime = None
    estado: str = None

@dataclass
class RevertirEtiquetado(EventoDominio):
    id: uuid.UUID = None
    id_anonimizado: uuid.UUID = None
    modalidad: uuid.UUID = None
    region_anatomica: str = None
    patologia: str = None
    fecha_creacion: datetime = None
    estado: str = None