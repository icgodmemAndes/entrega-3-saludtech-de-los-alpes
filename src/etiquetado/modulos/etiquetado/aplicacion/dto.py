import uuid
from dataclasses import dataclass

from etiquetado.seedwork.aplicacion.dto import DTO


@dataclass(frozen=True)
class EtiquetadoDTO(DTO):
    id_anonimizado: uuid.UUID
    modalidad: str
    region_anatomica: str
    patologia: str
    fecha_creacion: str | None = None
    estado: str


@dataclass(frozen=True)
class RevertirDTO(DTO):
    id_anonimizado: uuid.UUID
    modalidad: str
    region_anatomica: str
    patologia: str
    fecha_creacion: str | None = None
    estado: str