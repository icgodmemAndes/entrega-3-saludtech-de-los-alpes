from pulsar.schema import *
from aeroalpes.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class IngestaCreadaPayload(Record):
    id_proveedor = String()
    id_paciente = String()
    url_path = String()
    fecha_creacion = Long()

class EventoIngestaCreada(EventoIntegracion):
    data = IngestaCreadaPayload()

class IngestaFinalizadaPayload(Record):
    id_ingesta = String()
    fecha_actualizacion = Long()

class EventoIngestaFinalizada(EventoIntegracion):
    data = IngestaFinalizadaPayload()