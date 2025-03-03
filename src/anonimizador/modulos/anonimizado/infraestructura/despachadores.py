import pulsar
from pulsar.schema import *
from datetime import datetime

from anonimizador.modulos.anonimizado.infraestructura.schema.v1.comandos import (
    IniciarEtiquetado, IniciarEtiquetadoPayload, EliminarIngesta, EliminarIngestaPayload
)
from anonimizador.seedwork.infraestructura import utils

epoch = datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


class Despachador:
    def _publicar_mensaje_iniciar_etiquetado(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(IniciarEtiquetado))
        publicador.send(mensaje)
        cliente.close()

    def _publicar_mensaje_eliminar_ingesta(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(EliminarIngesta))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        raise NotImplementedError

    def publicar_comando_iniciar_etiquetado(self, comando, topico):
        payload = IniciarEtiquetadoPayload(
            id_anonimizado=str(comando.id),
            modalidad="TODO",
            region_anatomica="TODO",
            patologia="TODO"
        )
        comando_integracion = IniciarEtiquetado(data=payload)
        self._publicar_mensaje_iniciar_etiquetado(comando_integracion, topico, AvroSchema(IniciarEtiquetado))

    def publicar_comando_eliminar_ingesta(self, comando, topico):
        payload = EliminarIngestaPayload(
            id_ingesta=str(comando.id_ingesta),
        )
        comando_integracion = EliminarIngesta(data=payload)
        self._publicar_mensaje_eliminar_ingesta(comando_integracion, topico, AvroSchema(EliminarIngesta))
