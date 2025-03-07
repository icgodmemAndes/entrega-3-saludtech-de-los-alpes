import uuid
from dataclasses import dataclass

from etiquetado.seedwork.aplicacion.dto import DTO
from etiquetado.modulos.etiquetado.dominio.objetos_valor import EstadoEtiquetado


@dataclass(frozen=True)
class EtiquetadoDTO(DTO):
    id_anonimizado: uuid.UUID
    modalidad: str
    region_anatomica: str
    patologia: str
    estado: EstadoEtiquetado
    fecha_creacion: str | None = None


@dataclass(frozen=True)
class RevertirDTO(DTO):
    id_anonimizado: uuid.UUID
    modalidad: str
    region_anatomica: str
    patologia: str
    estado: EstadoEtiquetado
    fecha_creacion: str | None = None