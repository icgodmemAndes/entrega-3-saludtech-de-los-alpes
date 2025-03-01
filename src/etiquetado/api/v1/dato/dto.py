import uuid

from pydantic import BaseModel

class DistribuirDatos(BaseModel):
    id_proveedor: uuid.UUID
    id_paciente: uuid.UUID
    url_path: str
    estado: str
    etiquetas: list[str]
    modelo_utilizado: str
    confianza: float
