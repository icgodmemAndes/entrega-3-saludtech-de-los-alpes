import pulsar
from pulsar.schema import *

from sta.modulos.ingesta.infraestructura.schema.v1.eventos import EventoIngestaCreada, IngestaCreadaPayload
from sta.modulos.ingesta.infraestructura.schema.v1.comandos import ComandoCrearIngesta, ComandoCrearIngestaPayload
from sta.seedwork.infraestructura import utils

from datetime import datetime

epoch = datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(EventoIngestaCreada))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        payload = IngestaCreadaPayload(
            id_ingesta=str(evento.id),
            id_proveedor=str(evento.id_proveedor), 
            id_paciente=str(evento.id_paciente), 
            url_path=str(evento.url_path),
            estado=str(evento.estado),
            fecha_creacion=str(evento.fecha_creacion),
        )
        evento_integracion = EventoIngestaCreada(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoIngestaCreada))

    def publicar_comando(self, comando, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        payload = ComandoCrearIngestaPayload(
            id_proveedor=str(comando.id_proveedor), 
            id_paciente=str(comando.id_paciente), 
            url_path=str(comando.url_path)
        )
        comando_integracion = ComandoCrearIngesta(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoCrearIngesta))
