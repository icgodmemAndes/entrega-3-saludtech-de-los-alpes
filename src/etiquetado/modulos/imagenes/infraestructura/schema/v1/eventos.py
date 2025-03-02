from pulsar.schema import *
from etiquetado.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion


class EtiquetadoCreadaPayload(Record):
    id_etiquetado = String()
    id_proveedor = String()
    id_paciente = String()
    url_path = String()
    estado = String()
    fecha_creacion = String()


class EventoEtiquetadoCreada(EventoIntegracion):
    data = EtiquetadoCreadaPayload()


class ImagenProcesadaPayload(Record):
    id_imagen = String()
    id_etiquetado = String()
    estado = String()

class EliminarImagenPayload(Record):
    id_imagen = String()


class EventoImagenProcesada(EventoIntegracion):
    data = ImagenProcesadaPayload()

class EliminarImagen(EventoIntegracion):
    data = EliminarImagenPayload()
