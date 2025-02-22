from pulsar.schema import *
from sta.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class IngestaCreadaPayload(Record):
    id_ingesta = String()
    id_proveedor = String()
    id_paciente = String()
    url_path = String()
    estado = String()
    fecha_creacion = String()

class EventoIngestaCreada(EventoIntegracion):
    data = IngestaCreadaPayload()