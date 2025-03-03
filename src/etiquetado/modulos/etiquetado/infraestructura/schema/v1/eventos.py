from pulsar.schema import *
from etiquetado.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class EtiquetadoCreadaPayload(Record):
    id_etiquetado = String()
    id_anonimizado = String()
    modalidad = String()
    region_anatomica = String()
    patologia = String()
    fecha_creacion = String()

class EventoEtiquetadoCreada(EventoIntegracion):
    data = EtiquetadoCreadaPayload()