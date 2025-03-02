import pulsar, _pulsar
from pulsar.schema import *
import logging
import traceback

from etiquetado.modulos.imagenes.infraestructura.schema.v1.eventos import EventoEtiquetadoCreada
from etiquetado.seedwork.infraestructura import utils

from etiquetado.modulos.imagenes.dominio.entidades import Imagen
from .fabricas import FabricaRepositorio
from etiquetado.modulos.imagenes.dominio.fabricas import FabricaImagen
from .mapeadores import MapeadorImagen
from .repositorios import RepositorioImagen
from etiquetado.seedwork.infraestructura.uow import UnidadTrabajoPuerto

fabrica_imagen = FabricaImagen()
fabrica_repositorio = FabricaRepositorio()


def suscribirse_a_eventos(app):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-etiquetado', consumer_type=_pulsar.ConsumerType.Shared,
                                    subscription_name='etiquetado-sub-eventos', schema=AvroSchema(EventoEtiquetadoCreada))
        print('Consumiendo eventos de Etiquetado desde imagenes.....')

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido por Imagenes: {mensaje.value().data}')
            
            with app.app_context():
                try:
                    imagen: Imagen = fabrica_imagen.crear_objeto(mensaje.value().data, MapeadorImagen())
                    imagen.crear_imagen(imagen)
                    repositorio = fabrica_repositorio.crear_objeto(RepositorioImagen.__class__)

                    UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, imagen)
                    UnidadTrabajoPuerto.savepoint()
                    UnidadTrabajoPuerto.commit()
                except Exception as e:
                    print(f'Se presento un error procesando el eventos-etiquetado sobre las Imagenes. {e}')

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
        
