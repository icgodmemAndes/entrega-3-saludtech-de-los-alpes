import pulsar, _pulsar
from pulsar.schema import *
import uuid
import time
import logging
import traceback

from etiquetado.modulos.etiquetado.infraestructura.schema.v1.eventos import EventoEtiquetadoCreada
from etiquetado.modulos.etiquetado.infraestructura.schema.v1.comandos import ComandoCrearEtiquetado
from etiquetado.seedwork.infraestructura import utils
from etiquetado.modulos.etiquetado.aplicacion.comandos.crear_etiquetado import CrearEtiquetado
from etiquetado.modulos.etiquetado.aplicacion.comandos.revertir_etiquetado import RevertirEtiquetado
from etiquetado.seedwork.aplicacion.comandos import ejecutar_commando


def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-etiquetado', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='etiquetados-sub-eventos', schema=AvroSchema(EventoEtiquetadoCreada))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento eventos-etiquetado recibido: {mensaje.value().data}')

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
        consumidor = cliente.subscribe('comando-iniciar-etiquetado', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='etiquetado-sub-comando-iniciar-etiquetado',
                                       schema=AvroSchema(ComandoCrearEtiquetado))
        
        print('Consumiendo eventos de comando-iniciar-etiquetado desde Etiquetado.....')

        while True:
            mensaje = consumidor.receive()
            valor = mensaje.value()

            print(f'Comando comando-iniciar-etiquetado, recibido: {valor.data}')

            try:
                with app.app_context():
                    print("********* Paso Final *******************")
                    if valor.data.id_anonimizado[-1] in "abcdefghijklmABCDEFGHIJKLM12345":
                        print("************ Despacha CrearEtiquetado ********************")
                        comando = CrearEtiquetado(
                            id_anonimizado=uuid.UUID(valor.data.id_anonimizado),
                            modalidad=str(valor.data.modalidad),
                            region_anatomica=str(valor.data.region_anatomica),
                            patologia=str(valor.data.patologia),
                        )
                    else:
                        print("************* Despacha RevertirEtiquetado ****************")
                        comando = RevertirEtiquetado(
                            id_anonimizado=uuid.UUID(valor.data.id_anonimizado),
                            modalidad=str(valor.data.modalidad),
                            region_anatomica=str(valor.data.region_anatomica),
                            patologia=str(valor.data.patologia),
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
