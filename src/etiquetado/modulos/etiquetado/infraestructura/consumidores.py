import pulsar, _pulsar
from pulsar.schema import *
import uuid
import time
import logging
import traceback

from etiquetado.modulos.etiquetado.infraestructura.schema.v1.eventos import EventoEtiquetadoCreada
from etiquetado.modulos.etiquetado.infraestructura.schema.v1.comandos import ComandoCrearEtiquetado, ComandoEliminarEtiquetado
from etiquetado.seedwork.infraestructura import utils
from etiquetado.modulos.etiquetado.aplicacion.comandos.crear_etiquetado import CrearEtiquetado
from etiquetado.modulos.etiquetado.aplicacion.comandos.eliminar_etiquetado import EliminarEtiquetado
from etiquetado.seedwork.aplicacion.comandos import ejecutar_commando


def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-etiquetado', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='etiquetados-sub-eventos', schema=AvroSchema(EventoEtiquetadoCreada))

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


def suscribirse_a_comando_crear_etiquetado(app):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comando-crear-etiquetado', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='etiquetado-sub-comando-crear-etiquetado',
                                       schema=AvroSchema(ComandoCrearEtiquetado))
        
        print('Consumiendo eventos de Etiquetado desde Etiquetado.....')

        while True:
            mensaje = consumidor.receive()
            valor = mensaje.value()

            print(f'Comando etiquetado crear, recibido: {mensaje.value()}')

            try:
                with app.app_context():
                    comando = CrearEtiquetado(
                        id_anonimizado=uuid.UUID(valor.data.id_anonimizado),
                        modalidad=uuid.UUID(valor.data.modalidad),
                        region_anatomica=valor.data.region_anatomica,
                        patologia=valor.data.patologia
                    )

                    ejecutar_commando(comando)
            except:
                logging.error('ERROR: Procesando comando de creación de etiquetado!')
                traceback.print_exc()

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comando de creacion de etiquetado!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comando_eliminar_etiquetado(app):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comando-eliminar-etiquetado', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='etiquetado-sub-comando-eliminar-etiquetado',
                                       schema=AvroSchema(ComandoEliminarEtiquetado))

        while True:
            mensaje = consumidor.receive()
            valor = mensaje.value()

            print(f'Comando etiquetado crear, recibido: {mensaje.value()}')

            try:
                with app.app_context():
                    comando = EliminarEtiquetado(
                        id_etiquetado=uuid.UUID(valor.data.id_etiquetado),
                    )

                    ejecutar_commando(comando)
            except:
                logging.error('ERROR: Procesando comando de eliminacion de etiquetado!')
                traceback.print_exc()

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comando eliminacion de etiquetado!')
        traceback.print_exc()
        if cliente:
            cliente.close()