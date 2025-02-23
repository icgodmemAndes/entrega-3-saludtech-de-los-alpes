import pulsar
from pulsar.schema import *

from sta.modulos.imagenes.infraestructura.schema.v1.eventos import EventoImagenProcesada, ImagenProcesadaPayload
from sta.seedwork.infraestructura import utils

from datetime import datetime

epoch = datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(EventoImagenProcesada))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        payload = ImagenProcesadaPayload(
            id_imagen=str(evento.id),
            id_ingesta=str(evento.id_ingesta),
            estado=str(evento.estado),
        )
        evento_integracion = EventoImagenProcesada(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoImagenProcesada))

    def publicar_comando(self, comando, topico):
        raise NotImplementedError
