import pulsar
from pulsar.schema import *
from datetime import datetime

from anonimizador.modulos.anonimizado.infraestructura.schema.v1.comandos import (
     ComandoRevertirIngesta, ComandoRevertirIngestaPayLoad
)
from anonimizador.seedwork.infraestructura import utils

epoch = datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


class Despachador:

    def _publicar_mensaje_revertir_ingesta(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(ComandoRevertirIngesta))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        raise NotImplementedError

    def publicar_comando_revertir_ingesta(self, comando, topico):
        payload = ComandoRevertirIngestaPayLoad(
            id_ingesta=str(comando.id_ingesta),
        )

        print(f'publicando comando de compensacion a sta ...')

        comando_integracion = ComandoRevertirIngesta(data=payload)
        self._publicar_mensaje_revertir_ingesta(comando_integracion, topico, AvroSchema(ComandoRevertirIngesta))
