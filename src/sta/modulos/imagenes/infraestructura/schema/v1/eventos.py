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


class ImagenProcesadaPayload(Record):
    id_imagen = String()
    id_ingesta = String()
    estado = String()

class EliminarImagenPayload(Record):
    id_imagen = String()

class EventoImagenProcesada(EventoIntegracion):
    data = ImagenProcesadaPayload()

class EliminarImagen(EventoIntegracion):
    data = EliminarImagenPayload()

class IngestaRevertidaPayload(Record):
    id_ingesta = String()
    id_proveedor = String()
    id_paciente = String()
    url_path = String()
    estado = String()
    fecha_creacion = String()
    fecha_eliminacion = String()

class EventoIngestaRevertida(EventoIntegracion):
    data = IngestaCreadaPayload()