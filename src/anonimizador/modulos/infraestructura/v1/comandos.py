from pulsar.schema import *
from anonimizador.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)
from anonimizador.seedwork.infraestructura.utils import time_millis
import uuid


class LimpiarIngesta(Record):
    id = String()
    id_ingesta = String()


class EnriquecerImagen(Record):
    id = String()
    fecha_enriquecimiento = Long()
    tipo_imagen = String()

class ComandoEnriquecer(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    type = String(default="Enriquecer")
    datacontenttype = String()
    url_path = String()
    id_usuario = String()
    service_name = String(default="anonimizador.sta")
    data = EnriquecerImagen


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ComandoLimpiarIngesta(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="LimpiarIngesta")
    datacontenttype = String()
    service_name = String(default="anonimizador.sta")
    data = LimpiarIngesta

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

