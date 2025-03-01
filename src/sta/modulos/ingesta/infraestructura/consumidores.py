import pulsar, _pulsar
from pulsar.schema import *
import uuid
import time
import logging
import traceback

from sta.modulos.ingesta.infraestructura.schema.v1.eventos import EventoIngestaCreada
from sta.modulos.ingesta.infraestructura.schema.v1.comandos import ComandoCrearIngesta, ComandoEliminarIngesta
from sta.seedwork.infraestructura import utils

from sta.modulos.ingesta.aplicacion.comandos.crear_ingesta import CrearIngesta
from sta.seedwork.aplicacion.comandos import ejecutar_commando


def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-ingesta', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='sta-sub-eventos', schema=AvroSchema(EventoIngestaCreada))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_comandos(app):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comando-crear-ingesta', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='sta-sub-comando-crear-ingesta',
                                       schema=AvroSchema(ComandoCrearIngesta))
        
        consumidorEliminarIngesta = cliente.subscribe('comando-eliminar-ingesta', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='sta-sub-comandos', schema=AvroSchema(ComandoEliminarIngesta))
        print('Consumiendo eventos de Ingesta desde Ingesta.....')

        while True:
            mensaje = consumidor.receive()
            valor = mensaje.value()

            print(f'Comando ingesta crear, recibido: {mensaje.value()}')

            try:
                with app.app_context():
                    comando = CrearIngesta(
                        id_proveedor=uuid.UUID(valor.data.id_proveedor),
                        id_paciente=uuid.UUID(valor.data.id_paciente),
                        url_path=valor.data.url_path
                    )

                    ejecutar_commando(comando)
            except:
                logging.error('ERROR: Procesando comando de creación de ingesta!')
                traceback.print_exc()

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
