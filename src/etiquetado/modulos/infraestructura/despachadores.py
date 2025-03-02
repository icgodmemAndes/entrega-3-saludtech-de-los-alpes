import pulsar
from pulsar.schema import *

from etiquetado.modulos.infraestructura.v1.eventos import ImagenTageada, EventoImagenTageada
from etiquetado.modulos.infraestructura.v1.comandos import ComandoEnriquecer, EnriquecerImagen, TagearImagen, ComandoTagearImagen

from etiquetado.seedwork.infraestructura import utils

class Despachador:
    def __init__(self):
        ...

    def publicar_mensaje(self, mensaje, topico):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(mensaje.__class__))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento_imagen(self, evento, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        payload = ImagenTageada(
            id_proveedor=str(evento.id_proveedor),
            id_paciente=str(evento.id_paciente),
            url_path=str(evento.url_path),
            estado=str(evento.estado),
            etiquetas=evento.etiquetas,
            modelo_utilizado= str(evento.modelo_utilizado),
            confianza = float(evento.confianza)
        )
        evento_integracion = EventoImagenTageada(
            time=utils.time_millis(),
            datacontenttype=ImagenTageada.__name__,
            imagen_tageada=payload
        )
        self.publicar_mensaje(evento_integracion, topico)

    def publicar_comando_tagear(self, comando, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        payload = TagearImagen(
            id_proveedor=str(comando.id_proveedor),
            id_paciente=str(comando.id_paciente),
            url_path=str(comando.url_path),
            estado = str(comando.estado),
            modalidad = str(comando.modalidad),
            region_anatomica = str(comando.region_anatomica),
            patologia = str(comando.patologia),
            resolucion = str(comando.resolucion),
            contraste = str(comando.contraste),
            tipo = str(comando.tipo),
            fase = str(comando.fase),
            grupo_edad = str(comando.grupo_edad),
            sexo = str(comando.sexo),
            etnicidad = str(comando.etnicidad),
        )
        comando_integracion = ComandoTagearImagen(
            time=utils.time_millis(),
            datacontenttype=TagearImagen.__name__,
            data=payload
        )
        self.publicar_mensaje(comando_integracion, topico)