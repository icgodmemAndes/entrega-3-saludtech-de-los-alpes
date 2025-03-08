import logging
import traceback
import pulsar, _pulsar
from pulsar.schema import *

from anonimizador.modulos.anonimizado.infraestructura.schema.v1.eventos import EventoIngestaCreada
from anonimizador.seedwork.infraestructura import utils

from anonimizador.modulos.anonimizado.dominio.entidades import Anonimizado
from .fabricas import FabricaRepositorio
from anonimizador.modulos.anonimizado.dominio.fabricas import FabricaAnonimizado
from .mapeadores import MapeadorAnonimizado
from .repositorios import RepositorioAnonimizado
from anonimizador.seedwork.infraestructura.uow import UnidadTrabajoPuerto

fabrica_anonimizado = FabricaAnonimizado()
fabrica_repositorio = FabricaRepositorio()


def suscribirse_a_comando_iniciar_anonimizado(app):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comando-iniciar-anonimizado', consumer_type=_pulsar.ConsumerType.Shared,
                                    subscription_name='anonimizador-sub-comando-iniciar-anonimizado', schema=AvroSchema(EventoIngestaCreada))
        print('Consumiendo eventos de Anonimizador para comando-iniciar-anonimizado.....')

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido por anonimizador: {mensaje.value().data}')
            
            with app.app_context():
                try:
                    anonimizado: Anonimizado = fabrica_anonimizado.crear_objeto(mensaje.value().data, MapeadorAnonimizado())
                    anonimizado.crear_anonimizado(anonimizado)
                    repositorio = fabrica_repositorio.crear_objeto(RepositorioAnonimizado.__class__)

                    UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, anonimizado)
                    UnidadTrabajoPuerto.savepoint()
                    UnidadTrabajoPuerto.commit()
                except Exception as e:
                    print(f'Se presento un error procesando el comando-iniciar-anonimizado sobre las Anonimizador. {e}')

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos-ingesta desde Anonimizador!')
        traceback.print_exc()
        if cliente:
            cliente.close()
        
