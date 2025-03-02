import logging
import traceback
import _pulsar
import aiopulsar
from pulsar.schema import *
from anonimizador.seedwork.infraestructura import utils
from anonimizador.modulos.infraestructura.v1.eventos import IngestaCreada
from anonimizador.modulos.dominio.entidades import Ingesta

from .fabricas import FabricaRepositorio
from anonimizador.modulos.dominio.fabricas import FabricaImagen

from anonimizador.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from anonimizador.modulos.dominio.repositorios import RepositorioImagen
from anonimizador.modulos.infraestructura.mapeadores import MapeadorImagen
from anonimizador.modulos.infraestructura.despachadores import Despachador
from anonimizador.modulos.dominio.objetos_valor import EstadoIngesta

from anonimizador.modulos.infraestructura.v1.comandos import ComandoLimpiarIngesta, LimpiarIngesta, EnriquecerImagen
from typing import List, Dict, Any, Type, Callable


despachador = Despachador()

fabrica_imagen = FabricaImagen()
fabrica_repositorio = FabricaRepositorio()


async def suscribirse_a_topico(topico: str, suscripcion: str, schema: Record, tipo_consumidor:_pulsar.ConsumerType=_pulsar.ConsumerType.Shared):
    try:
        schema_original = schema
        async with aiopulsar.connect(f'pulsar://{utils.broker_host()}:6650') as anonimizador:
            async with anonimizador.subscribe(
                topico, 
                consumer_type=tipo_consumidor,
                subscription_name=suscripcion, 
                schema=AvroSchema(schema)
            ) as consumidor:
                while True:
                    print(f'Escuchando mensajes...')
                    mensaje = await consumidor.receive()
                    print(f'{mensaje.__dict__}')

                    print(f'Evento recibido por Anonimizador: {mensaje.value()}')               
                    #dependiendo del tipo de evento, se realiza una acción
                    try:
                        ingesta: Ingesta = fabrica_imagen.crear_objeto(mensaje.value(), MapeadorImagen())
                        
                        ingesta.crear_imagen(ingesta)
                        repositorio = fabrica_repositorio.crear_objeto(RepositorioImagen.__class__)
                        print(f'Ingesta mapeada {ingesta.__dict__}')
                                             
                        #publicar mensaje para limipiar ingesta
                        payload_limpieza = LimpiarIngesta(id_ingesta=ingesta.id_ingesta)
                        despachador.publicar_mensaje(payload_limpieza, "comando-eliminar-ingesta")
                        

                        print(f'-> Se despacha comando limpieza: {payload_limpieza.__dict__}')

                        #publicar mensaje para enriquecer ingesta
                        payload_enriquecer =  EnriquecerImagen(
                            id_proveedor = ingesta.id_proveedor,
                            id_paciente = ingesta.id_paciente,
                            url_path = ingesta.url_path,
                            estado = EstadoIngesta.ANONIMIZADA,
                            modalidad = "Rayos X",
                            region_anatomica = "Cerebro",
                            patologia = "Tumor",
                            resolucion = "1920x1080",
                            contraste = "Alto",
                            tipo = "2D",
                            fase = "Pre-tratamiento",
                            grupo_edad = "Adulto",
                            sexo = "Masculino",
                            etnicidad = "Latino",
                        )
                        
                        despachador.publicar_mensaje(payload_enriquecer, "comando-enriquecer")
                        print(f'-> Se despacha comando enriquecer: {payload_enriquecer.__dict__}')

                     
                        print('antes de guardar')
                        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, ingesta)
                        UnidadTrabajoPuerto.savepoint()
                        UnidadTrabajoPuerto.commit()
                        print(f'Ingesta guardada {ingesta.__dict__}')
                        
                    except Exception as e:
                        #traceback.print_exc()
                        print(f'Se presento un error procesando la anonimizacion escuchando el topico {topico}. {e}')

                    datos = mensaje.value()
                    print(f'Evento recibido: {datos}')
                    await consumidor.acknowledge(mensaje)    

    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()




