import uuid
from pulsar.schema import *
from anonimizador.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion
from anonimizador.seedwork.infraestructura.utils import time_millis


class IniciarEtiquetadoPayload(Record):
    id_anonimizado = String()
    modalidad = String()
    region_anatomica = String()
    patologia = String()


class IniciarEtiquetado(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = IniciarEtiquetadoPayload()


class EliminarIngestaPayload(Record):
    id_ingesta = String()


class EliminarIngesta(ComandoIntegracion):
    data = EliminarIngestaPayload()
