import pulsar, _pulsar
from pulsar.schema import *
import logging
import traceback

from sta.modulos.imagenes.infraestructura.schema.v1.eventos import EventoIngestaCreada
from sta.seedwork.infraestructura import utils

from sta.modulos.imagenes.dominio.entidades import Imagen
from .fabricas import FabricaRepositorio
from sta.modulos.imagenes.dominio.fabricas import FabricaImagen
from .mapeadores import MapeadorImagen
from .repositorios import RepositorioImagen
from sta.seedwork.infraestructura.uow import UnidadTrabajoPuerto

fabrica_imagen = FabricaImagen()
fabrica_repositorio = FabricaRepositorio()


def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-ingesta', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='sta-sub-eventos', schema=AvroSchema(EventoIngestaCreada))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido por Imagenes: {mensaje.value().data}')

            #imagen: Imagen = fabrica_imagen.crear_objeto(mensaje.value().data, MapeadorImagen())
            #imagen.crear_imagen(imagen)
            #repositorio = fabrica_repositorio.crear_objeto(RepositorioImagen.__class__)
            
            #UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, imagen)
            #UnidadTrabajoPuerto.savepoint()
            #UnidadTrabajoPuerto.commit()

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
