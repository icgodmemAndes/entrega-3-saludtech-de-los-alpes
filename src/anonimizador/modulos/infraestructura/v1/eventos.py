from pulsar.schema import *
from anonimizador.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from anonimizador.seedwork.infraestructura.utils import time_millis

import uuid

class IngestaCreada(Record):
    id_ingesta = String()
    id_proveedor = String()
    id_paciente = String()
    url_path = String()
    estado = String()
    fecha_creacion = String()


class ImagenAnonimizada(Record):
    id = String()
    id_ingesta = String()
    url_path = String()


class EventoAnonimizacion(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="EventoAnonimizacionImagen")
    datacontenttype = String()
    service_name = String(default="anonimizador.sta")
    inagen_anonimizada = ImagenAnonimizada

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)