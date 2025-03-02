import uuid
from dataclasses import dataclass

from etiquetado.seedwork.aplicacion.dto import DTO


@dataclass(frozen=True)
class EtiquetadoDTO(DTO):
    id_proveedor: uuid.UUID
    id_paciente: uuid.UUID
    url_path: str
    estado: str
    fecha_creacion: str | None = None