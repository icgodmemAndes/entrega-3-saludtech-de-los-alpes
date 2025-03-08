import pulsar
from pulsar.schema import *

from etiquetado.modulos.etiquetado.infraestructura.schema.v1.eventos import EventoEtiquetadoCreada, EtiquetadoCreadaPayload
from etiquetado.modulos.etiquetado.infraestructura.schema.v1.comandos import ComandoCrearEtiquetado, ComandoCrearEtiquetadoPayload,RevertirEtiquetadoPayload,RevertirEtiquetado
from etiquetado.seedwork.infraestructura import utils

from datetime import datetime

epoch = datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(EventoEtiquetadoCreada))
        publicador.send(mensaje)
        cliente.close()
    def _publicar_mensaje_revertir_etiquetado(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(RevertirEtiquetado))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        payload = EtiquetadoCreadaPayload(
            id_etiquetado=str(evento.id),
            id_anonimizado=str(evento.id_anonimizado), 
            modalidad=str(evento.modalidad), 
            region_anatomica=str(evento.region_anatomica),
            patologia=str(evento.patologia),
            fecha_creacion=str(evento.fecha_creacion),
            estado=str(evento.estado)
        )
        evento_integracion = EventoEtiquetadoCreada(data=payload)
        print("****evento integracion****")
        print(payload)
        print(payload.estado)
        print(evento_integracion)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoEtiquetadoCreada))

    def publicar_comando(self, comando, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        payload = ComandoCrearEtiquetadoPayload(
            id_anonimizado=str(comando.id_anonimizado), 
            modalidad=str(comando.modalidad), 
            region_anatomica=str(comando.region_anatomica),
            patologia=str(comando.patologia)
        )
        comando_integracion = ComandoCrearEtiquetado(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoCrearEtiquetado))

    def publicar_comando_revertir_etiquetado(self, comando, topico):
        payload = RevertirEtiquetadoPayload(
            id_anonimizado=str(comando.id_anonimizado),
        )
        comando_integracion = RevertirEtiquetado(data=payload)
        self._publicar_mensaje_revertir_etiquetado(comando_integracion, topico, AvroSchema(RevertirEtiquetado))
