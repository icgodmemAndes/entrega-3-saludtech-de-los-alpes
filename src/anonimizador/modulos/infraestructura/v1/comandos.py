from pulsar.schema import *
from anonimizador.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)
from anonimizador.seedwork.infraestructura.utils import time_millis
import uuid


class LimpiarIngesta(Record):
    id = String()
    id_ingesta = String()


class IngestaCreadaPayload(Record):
    id_ingesta = String()
    id_proveedor = String()
    id_paciente = String()
    url_path = String()
    estado = String()
    fecha_creacion = String()


class EnriquecerImagen(Record):
    id_proveedor = String(),
    id_paciente = String(),
    url_path = String(),
    estado = String(),
    modalidad = String(),
    region_anatomica = String(),
    patologia = String(),
    resolucion = String(),
    contraste = String(),
    tipo = String(),
    fase = String(),
    grupo_edad = String(),
    sexo = String(),
    etnicidad = String()

class ComandoEnriquecer(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="Enriquecer")
    datacontenttype = String()
    service_name = String(default="etiquetado.sta")
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

