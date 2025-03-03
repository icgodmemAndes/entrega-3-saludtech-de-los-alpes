from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from etiquetado.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime


@dataclass
class EtiquetadoCreada(EventoDominio):
    id: uuid.UUID = None
    id_proveedor: uuid.UUID = None
    id_paciente: uuid.UUID = None
    url_path: str = None
    fecha_creacion: datetime = None
    estado: str = None

@dataclass
class EtiquetadoEliminada(EventoDominio):
    id: uuid.UUID = None
    fecha_eliminacion: datetime = None
    estado: str = None

@dataclass
class Tagear(EventoDominio):
    id: uuid.UUID = None
    id_anonimizada: uuid.UUID = None