import pulsar
from pulsar.schema import *

from sta.modulos.ingesta.infraestructura.schema.v1.eventos import EventoIngestaCreada, IngestaCreadaPayload, EventoIngestaRevertida, IngestaRevertidaPayload, EventoIngestaEliminada, IngestaEliminadaPayLoad, EventoIngestaAlertada, IngestaAlertadaPayLoad
from sta.modulos.ingesta.infraestructura.schema.v1.comandos import ComandoCrearIngesta, ComandoCrearIngestaPayload, ComandoIniciarAnonimizado, ComandoIniciarAnonimizadoPayload
from sta.seedwork.infraestructura import utils

from datetime import datetime

epoch = datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()
    
    def publicar_evento_ingesta_creada(self, evento, topico):
        payload = IngestaCreadaPayload(
            id_ingesta=str(evento.id),
            id_proveedor=str(evento.id_proveedor), 
            id_paciente=str(evento.id_paciente), 
            url_path=str(evento.url_path),
            estado=str(evento.estado),
            fecha_creacion=str(evento.fecha_creacion),
        )
        evento_integracion = EventoIngestaCreada(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoIngestaCreada))
    
    def publicar_evento_ingesta_revertida(self, evento, topico):
        payload = IngestaRevertidaPayload(
            id_ingesta=str(evento.id),
            id_proveedor=str(evento.id_proveedor), 
            id_paciente=str(evento.id_paciente), 
            url_path=str(evento.url_path),
            estado=str(evento.estado),
            fecha_creacion=str(evento.fecha_creacion),
            fecha_eliminacion=str(evento.fecha_eliminacion),
        )

        evento_integracion = EventoIngestaRevertida(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoIngestaRevertida))


    def publicar_evento_ingesta_eliminada(self, evento, topico):
        payload = IngestaEliminadaPayLoad(
            id_ingesta=str(evento.id),
            estado=str(evento.estado),
            fecha_eliminacion=str(evento.fecha_eliminacion),
        )
        evento_integracion = EventoIngestaEliminada(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoIngestaEliminada))

    def publicar_comando(self, comando, topico):
        payload = ComandoCrearIngestaPayload(
            id_proveedor=str(comando.id_proveedor), 
            id_paciente=str(comando.id_paciente), 
            url_path=str(comando.url_path)
        )
        comando_integracion = ComandoCrearIngesta(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoCrearIngesta))

    def publicar_comando_iniciar_anonimizado(self, comando, topico):
        payload = ComandoIniciarAnonimizadoPayload(
            id_ingesta=str(comando.id),
            id_proveedor=str(comando.id_proveedor), 
            id_paciente=str(comando.id_paciente), 
            url_path=str(comando.url_path)
        )
        comando_integracion = ComandoIniciarAnonimizado(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoIniciarAnonimizado))
    
    def publicar_evento_ingesta_alertada(self, evento, topico):
        payload = IngestaAlertadaPayLoad(
            id_ingesta=str(evento.id),
            estado=str(evento.estado),
        )
        evento_integracion = EventoIngestaAlertada(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoIngestaAlertada))