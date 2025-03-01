from pulsar.schema import *
from etiquetado.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from etiquetado.seedwork.infraestructura.utils import time_millis

import uuid

class ImagenTageada(Record):
    id_proveedor: String()
    id_paciente: String()
    url_path: String()
    estado: String()
    etiquetas: Array(String())
    modelo_utilizado: String()
    confianza: Float()

class EventoImagenTageada(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    datacontenttype = String()
    type = String(default="EventoImagenTageada")
    service_name = String(default="etiquetado.sta")
    imagen_tageada = ImagenTageada

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)