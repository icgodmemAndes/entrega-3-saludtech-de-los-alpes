from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from sta.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime


@dataclass
class IniciarAnonimizado(EventoDominio):
    id: uuid.UUID = None
    id_proveedor: uuid.UUID = None
    id_paciente: uuid.UUID = None
    url_path: str = None
    fecha_creacion: datetime = None
    estado: str = None

@dataclass
class IngestaEliminada(EventoDominio):
    id: uuid.UUID = None
    fecha_eliminacion: datetime = None
    estado: str = None

@dataclass
class IngestaRevertida(EventoDominio):
    id: uuid.UUID = None
    estado: str = None
    id_proveedor: uuid.UUID = None
    id_paciente: uuid.UUID = None
    url_path: str = None
    fecha_creacion: datetime = None
    fecha_eliminacion: datetime = None