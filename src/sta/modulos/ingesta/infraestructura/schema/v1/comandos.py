from pulsar.schema import *
from dataclasses import dataclass, field
from sta.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)
from sta.seedwork.infraestructura.utils import time_millis
import uuid

class ComandoCrearIngestaPayload(Record):
    id_proveedor = String()
    id_paciente = String()
    url_path = String()

class ComandoIniciarAnonimizadoPayload(Record):
    id_ingesta = String()
    id_proveedor = String()
    id_paciente = String()
    url_path = String()

class ComandoEliminarIngestaPayLoad(Record):
    id_ingesta = String()

class ComandoRevertirIngestaPayLoad(Record):
    id_ingesta = String()

class ComandoCrearIngesta(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = ComandoCrearIngestaPayload()

class ComandoIniciarAnonimizado(ComandoIntegracion):
    data = ComandoIniciarAnonimizadoPayload()

class ComandoEliminarIngesta(ComandoIntegracion):
    data = ComandoEliminarIngestaPayLoad()

class ComandoRevertirIngesta(ComandoIntegracion):
    data = ComandoRevertirIngestaPayLoad()