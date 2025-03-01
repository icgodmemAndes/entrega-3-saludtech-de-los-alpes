import uuid
from dataclasses import dataclass

from sta.seedwork.aplicacion.dto import DTO


@dataclass(frozen=True)
class IngestaDTO(DTO):
    id_proveedor: uuid.UUID
    id_paciente: uuid.UUID
    url_path: str
    estado: str
    fecha_creacion: str | None = None