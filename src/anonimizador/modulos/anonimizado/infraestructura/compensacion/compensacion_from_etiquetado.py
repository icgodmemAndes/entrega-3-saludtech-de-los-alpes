import logging
import traceback
import pulsar, _pulsar
from pulsar.schema import *

from anonimizador.modulos.anonimizado.infraestructura.schema.v1.comandos import ComandoCompensacionEtiquetado
from anonimizador.seedwork.infraestructura import utils

from anonimizador.modulos.anonimizado.dominio.entidades import Anonimizado
from anonimizador.modulos.anonimizado.infraestructura.fabricas import FabricaRepositorio
from anonimizador.modulos.anonimizado.dominio.fabricas import FabricaAnonimizado
from anonimizador.modulos.anonimizado.infraestructura.mapeadores import MapeadorRevertirAnonimizado
from anonimizador.modulos.anonimizado.infraestructura.repositorios import RepositorioAnonimizado
from anonimizador.seedwork.infraestructura.uow import UnidadTrabajoPuerto

fabrica_anonimizado = FabricaAnonimizado()
fabrica_repositorio = FabricaRepositorio()


def suscribirse_a_comando_compensacion(app):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comando-revertir-anonimizado', consumer_type=_pulsar.ConsumerType.Shared,
                                    subscription_name='anonimizador-compensacion-comando-revertir-anonimizado', schema=AvroSchema(ComandoCompensacionEtiquetado))
        print('[/] Escuchando por comandos de compensacion comando-revertir-anonimizado por parte de Etiquetado.....')

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido por anonimizador - comando-revertir-anonimizado: {mensaje.value().data}')
            
            with app.app_context():
                try:
                    anonimizado : Anonimizado = Anonimizado(mensaje.value().data.id_anonimizado)
                    print(f'Comando recibido y mapeado: {anonimizado.__dict__}')
                    
                    #consulto el anonimizado en la base de datos
                    anonimizado = anonimizado.revertir(anonimizado)
                    repositorio = fabrica_repositorio.crear_objeto(RepositorioAnonimizado.__class__)
                                        
                    #Cargar la entidad anonimizado con el estado revertido en la Unidad de Trabajo
                    UnidadTrabajoPuerto.registrar_batch(repositorio.revertir_anonimizado, anonimizado)
                    UnidadTrabajoPuerto.savepoint()
                    UnidadTrabajoPuerto.commit()
                except Exception as e:
                    print(f'Se presento un error procesando la compensacion desde etiquetado {e}')

            consumidor.acknowledge(mensaje)

    except:
        logging.error('ERROR: Suscribiendose al tópico de comando-revertir-anonimizado desde Anonimizador!')
        traceback.print_exc()
        if cliente:
            cliente.close()
        
