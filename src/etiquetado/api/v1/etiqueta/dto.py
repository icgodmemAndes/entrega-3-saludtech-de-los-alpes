import uuid

from pydantic import BaseModel

class TagearImagen(BaseModel):
    id_proveedor: uuid.UUID
    id_paciente: uuid.UUID
    url_path: str
    estado: str
    modalidad: str
    region_anatomica: str
    patologia: str
    resolucion: str
    contraste: str
    tipo: str
    fase: str
    grupo_edad: str
    sexo: str
    etnicidad: str