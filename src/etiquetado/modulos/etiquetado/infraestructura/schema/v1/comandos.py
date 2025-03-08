from pulsar.schema import *
from dataclasses import dataclass, field
from etiquetado.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)
from etiquetado.seedwork.infraestructura.utils import time_millis
import uuid


class ComandoCrearEtiquetadoPayload(ComandoIntegracion):
    id_anonimizado = String()
    modalidad = String()
    region_anatomica = String()
    patologia = String()

class ComandoCrearEtiquetado(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = ComandoCrearEtiquetadoPayload()

class RevertirEtiquetadoPayload(ComandoIntegracion):
    id_anonimizado = String()


class RevertirEtiquetado(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = RevertirEtiquetadoPayload()

