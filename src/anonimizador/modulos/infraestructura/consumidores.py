import logging
import traceback
import _pulsar
import aiopulsar
from pulsar.schema import *
from anonimizador.seedwork.infraestructura import utils
from anonimizador.modulos.infraestructura.v1.eventos import IngestaCreada
from anonimizador.modulos.dominio.entidades import Imagen

from .fabricas import FabricaRepositorio
from anonimizador.modulos.dominio.fabricas import FabricaImagen

from anonimizador.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from anonimizador.modulos.dominio.repositorios import RepositorioImagen
from anonimizador.modulos.infraestructura.mapeadores import MapeadorImagen


fabrica_imagen = FabricaImagen()
fabrica_repositorio = FabricaRepositorio()


async def suscribirse_a_topico(topico: str, suscripcion: str, schema: Record, tipo_consumidor:_pulsar.ConsumerType=_pulsar.ConsumerType.Shared):
    try:
        async with aiopulsar.connect(f'pulsar://{utils.broker_host()}:6650') as anonimizador:
            async with anonimizador.subscribe(
                topico, 
                consumer_type=tipo_consumidor,
                subscription_name=suscripcion, 
                schema=AvroSchema(schema)
            ) as consumidor:
                while True:
                    mensaje = await consumidor.receive()
                    print(f'Evento recibido por Anonimizador: {mensaje.value().data}')

                    #dependiendo del tipo de evento, se realiza una acción
                    if isinstance(schema, IngestaCreada):
                        try:
                            imagen: Imagen = fabrica_imagen.crear_objeto(mensaje.value().data, MapeadorImagen())
                            imagen.crear_imagen(imagen)
                            repositorio = fabrica_repositorio.crear_objeto(RepositorioImagen.__class__)

                            UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, imagen)
                            UnidadTrabajoPuerto.savepoint()
                            UnidadTrabajoPuerto.commit()
                            
                        except Exception as e:
                            print(f'Se presento un error procesando el eventos-ingesta sobre las Imagenes. {e}')

                    datos = mensaje.value()
                    print(f'Evento recibido: {datos}')
                    await consumidor.acknowledge(mensaje)    

    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()



