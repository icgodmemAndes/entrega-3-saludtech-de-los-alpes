from __future__ import annotations
from dataclasses import dataclass, field
from aeroalpes.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime


@dataclass
class IngestaCreada(EventoDominio):
    id_proveedor: uuid.UUID = None
    id_paciente: uuid.UUID = None
    url_path: str = None
    fecha_creacion: datetime = None
    estado: str = None

@dataclass
class IngestaFinalizada(EventoDominio):
    id_ingesta: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class IngestaRechazada(EventoDominio):
    id_ingesta: uuid.UUID = None
    fecha_actualizacion: datetime = None