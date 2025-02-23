from pulsar.schema import *
from dataclasses import dataclass, field
from sta.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearIngestaPayload(ComandoIntegracion):
    id_proveedor = String()
    id_paciente = String()
    url_path = String()

class ComandoCrearIngesta(ComandoIntegracion):
    data = ComandoCrearIngestaPayload()