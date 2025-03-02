import logging
import traceback
import pulsar, _pulsar
import aiopulsar
import asyncio
from pulsar.schema import *
from etiquetado.seedwork.infraestructura import utils

from etiquetado.modulos.infraestructura.v1.comandos import EnriquecerImagen

from .fabricas import FabricaRepositorio
from etiquetado.modulos.dominio.fabricas import FabricaImagen

from etiquetado.seedwork.infraestructura.uow import UnidadTrabajoPuertoAsync
from etiquetado.modulos.dominio.repositorios import RepositorioImagen
from etiquetado.modulos.infraestructura.mapeadores import MapeadorImagen

from etiquetado.modulos.dominio.entidades import Imagen

fabrica_imagen = FabricaImagen()
fabrica_repositorio = FabricaRepositorio()


async def suscribirse_a_topico(topico: str, suscripcion: str, schema: Record, tipo_consumidor:_pulsar.ConsumerType=_pulsar.ConsumerType.Shared):
    try:
        async with aiopulsar.connect(f'pulsar://{utils.broker_host()}:6650') as cliente:
            async with cliente.subscribe(
                topico, 
                consumer_type=tipo_consumidor,
                subscription_name=suscripcion, 
                schema=AvroSchema(schema)
            ) as consumidor:
                while True:
                    mensaje = await consumidor.receive()
                    print(mensaje)
                    print('***************Trata de guardar****************')
                    try:
                        imagen: Imagen = fabrica_imagen.crear_objeto(mensaje.value().data, MapeadorImagen())
                        print('***************Mapeo hecho****************')
                        #imagen.tagear_imagen(imagen)
                        print('***************Trata de guardar****************')
                        repositorio = fabrica_repositorio.crear_objeto(RepositorioImagen.__class__)
                        print('***************Envia a uow****************')
                        UnidadTrabajoPuertoAsync.registrar_batch(repositorio.agregar, imagen)
                        UnidadTrabajoPuertoAsync.savepoint()
                        UnidadTrabajoPuertoAsync.commit()

                    except Exception as e:
                        print(f'Se presento un error procesando el eventos-ingesta sobre las Imagenes. {e}')
                        traceback.print_exc()
                    datos = mensaje.value()
                    print(f'Evento recibido: {datos}')
                    await consumidor.acknowledge(mensaje)    

    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()