import pulsar, _pulsar
from pulsar.schema import *
import logging
import traceback

from sta.modulos.imagenes.infraestructura.schema.v1.eventos import EventoIngestaCreada, EventoIngestaRevertida
from sta.seedwork.infraestructura import utils

from sta.modulos.imagenes.dominio.entidades import Imagen
from .fabricas import FabricaRepositorio
from sta.modulos.imagenes.dominio.fabricas import FabricaImagen
from .mapeadores import MapeadorImagen
from .repositorios import RepositorioImagen
from sta.seedwork.infraestructura.uow import UnidadTrabajoPuerto

fabrica_imagen = FabricaImagen()
fabrica_repositorio = FabricaRepositorio()


def suscribirse_a_evento_ingesta_creada(app):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('evento-ingesta-creada', consumer_type=_pulsar.ConsumerType.Shared,
                                    subscription_name='sta-sub-evento-ingesta-creada', schema=AvroSchema(EventoIngestaCreada))
        print('Consumiendo evento de evento-ingesta-creada desde Imagenes.....')

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido desde evento-ingesta-creada por Imagenes: {mensaje.value().data}')
            
            with app.app_context():
                try:
                    imagen: Imagen = fabrica_imagen.crear_objeto(mensaje.value().data, MapeadorImagen())
                    imagen.crear_imagen(imagen)
                    repositorio = fabrica_repositorio.crear_objeto(RepositorioImagen.__class__)

                    UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, imagen)
                    UnidadTrabajoPuerto.savepoint()
                    UnidadTrabajoPuerto.commit()
                except Exception as e:
                    print(f'Se presento un error procesando el evento ingesta-creada sobre las Imagenes. {e}')

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
        
def suscribirse_a_evento_ingesta_revertida(app):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('evento-ingesta-revertida', consumer_type=_pulsar.ConsumerType.Shared,
                                    subscription_name='sta-sub-evento-ingesta-revertida', schema=AvroSchema(EventoIngestaRevertida))
        print('Consumiendo evento de evento-ingesta-revertida desde Imagenes.....')

        while True:
            mensaje = consumidor.receive()
            valor = mensaje.value()

            print(f'Evento recibido desde evento-ingesta-revertida por Imagenes: {valor.data}')
            
            with app.app_context():
                try:
                    repositorio = fabrica_repositorio.crear_objeto(RepositorioImagen.__class__)
                    imagen: Imagen = repositorio.obtener_por_id_ingesta(valor.data.id_ingesta)
                    imagen.revertir_imagen()

                    UnidadTrabajoPuerto.registrar_batch(repositorio.revertir, imagen)
                    UnidadTrabajoPuerto.savepoint()
                    UnidadTrabajoPuerto.commit()
                except Exception as e:
                    print(f'Se presento un error procesando el evento ingesta-revertida sobre las Imagenes. {e}')

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()