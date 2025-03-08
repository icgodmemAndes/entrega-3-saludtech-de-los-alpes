import pulsar, _pulsar
from pulsar.schema import *
import uuid
import logging
import traceback
import random

from sta.modulos.ingesta.infraestructura.schema.v1.comandos import ComandoCrearIngesta, ComandoEliminarIngesta, ComandoRevertirIngesta
from sta.seedwork.infraestructura import utils
from sta.modulos.ingesta.aplicacion.comandos.crear_ingesta import CrearIngesta
from sta.modulos.ingesta.aplicacion.comandos.eliminar_ingesta import EliminarIngesta
from sta.modulos.ingesta.aplicacion.comandos.revertir_ingesta import RevertirIngesta
from sta.modulos.ingesta.aplicacion.comandos.alerta_ingesta import AlertaIngesta
from sta.seedwork.aplicacion.comandos import ejecutar_commando


def suscribirse_a_comando_crear_ingesta(app):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comando-crear-ingesta', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='sta-sub-comando-crear-ingesta',
                                       schema=AvroSchema(ComandoCrearIngesta))

        print('Consumiendo eventos de comando-crear-ingesta desde Ingesta.....')

        while True:
            mensaje = consumidor.receive()
            valor = mensaje.value()

            print(f'mensaje de comando-crear-ingesta, recibido: {valor.data}')

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
        logging.error('ERROR: Suscribiendose al tópico de comando de creacion de ingesta!')
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_comando_eliminar_ingesta(app):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comando-eliminar-ingesta', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='sta-sub-comando-eliminar-ingesta',
                                       schema=AvroSchema(ComandoEliminarIngesta))

        while True:
            mensaje = consumidor.receive()
            valor = mensaje.value()

            print(f'mensaje de comando-eliminar-ingesta, recibido: {valor.data}')

            try:
                with app.app_context():
                    if random.randint(0, 10) <= 3:
                        comando = EliminarIngesta(
                            id_ingesta=uuid.UUID(valor.data.id_ingesta),
                        )
                    else:
                        comando = AlertaIngesta(
                            id_ingesta=uuid.UUID(valor.data.id_ingesta),
                        )

                    ejecutar_commando(comando)
            except:
                logging.error('ERROR: Procesando comando de eliminacion de ingesta!')
                traceback.print_exc()

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comando eliminacion de ingesta!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comando_revertir_ingesta(app):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comando-revertir-ingesta', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='sta-sub-comando-elimin-ingesta',
                                       schema=AvroSchema(ComandoRevertirIngesta))

        while True:
            mensaje = consumidor.receive()
            valor = mensaje.value()

            print(f'mensaje de comando-revertir-ingesta, recibido: {valor.data}')

            try:
                with app.app_context():
                    comando = RevertirIngesta(
                        id_ingesta=uuid.UUID(valor.data.id_ingesta),
                    )

                    ejecutar_commando(comando)
            except:
                logging.error('ERROR: Procesando comando de reversion de ingesta!')
                traceback.print_exc()

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comando reversion de ingesta!')
        traceback.print_exc()
        if cliente:
            cliente.close()