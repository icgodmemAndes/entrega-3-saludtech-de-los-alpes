from pulsar.schema import *
from aeroalpes.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class IngestaCreadaPayload(Record):
    id_proveedor = String()
    id_paciente = String()
    url_path = String()

class EventoIngestaCreada(EventoIntegracion):
    data = IngestaCreadaPayload()