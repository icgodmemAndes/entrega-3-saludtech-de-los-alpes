import pulsar
from pulsar.schema import *
from datetime import datetime

from anonimizador.modulos.anonimizado.infraestructura.schema.v1.comandos import (
    IniciarEtiquetado, IniciarEtiquetadoPayload, EliminarIngesta, EliminarIngestaPayload, ComandoRevertirIngesta, ComandoRevertirIngestaPayLoad
)
from anonimizador.seedwork.infraestructura import utils
import random

epoch = datetime.utcfromtimestamp(0)

modalidades = ["rayos-x", "ecografia", "resonancia_magnetica", "tomografia_computarizada", 
            "ultrasonido", "mamografia", "angiografia", "fluoroscopia", "endoscopia", 
            "radiografia", "medicina_nuclear", "tomografia_por_emision_de_positrones", 
            "densitometria_osea", "termografia", "electrocardiograma", "electroencefalograma", 
            "electrorretinografia", "electromiografia", "radiologia_intervencionista", "gammagrafia"]

regiones_anatomicas = ["pulmon", "cabeza", "cerebro", "corazon", "higado", "rinon", "estomago", 
                "intestino", "columna_vertebral", "extremidades_superiores", "extremidades_inferiores", 
                "cuello", "torax", "abdomen", "pelvis", "ojos", "oidos", "nariz", "boca", "piel"]

patologias = ["neumonia", "cancer", "fractura", "infeccion", "tumor", "inflamacion", "diabetes", 
            "hipertension", "insuficiencia_cardiaca", "derrame_cerebral", "enfermedad_de_Alzheimer", 
            "artritis", "osteoporosis", "enfermedad_de_Parkinson", "esclerosis_multiple", 
            "enfermedad_renal", "cirrosis", "ulcera", "migrana", "asma"]

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


class Despachador:
    def _publicar_mensaje_iniciar_etiquetado(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(IniciarEtiquetado))
        publicador.send(mensaje)
        cliente.close()

    def _publicar_mensaje_eliminar_ingesta(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(EliminarIngesta))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        raise NotImplementedError

    def publicar_comando_iniciar_etiquetado(self, comando, topico):
        # Definir listas de opciones para los campos        
        # Generar datos aleatorios
        
        modalidad = random.choice(modalidades) if modalidades else 'None'
        region = random.choice(regiones_anatomicas) if regiones_anatomicas else 'None'
        patologia = random.choice(patologias) if patologias else 'None'
        
        payload = IniciarEtiquetadoPayload(
            id_anonimizado=str(comando.id),
            modalidad=modalidad,
            region_anatomica=region,
            patologia=patologia
        )
        comando_integracion = IniciarEtiquetado(data=payload)
        self._publicar_mensaje_iniciar_etiquetado(comando_integracion, topico, AvroSchema(IniciarEtiquetado))

    def publicar_comando_eliminar_ingesta(self, comando, topico):
        payload = EliminarIngestaPayload(
            id_ingesta=str(comando.id_ingesta),
        )
        comando_integracion = EliminarIngesta(data=payload)
        self._publicar_mensaje_eliminar_ingesta(comando_integracion, topico, AvroSchema(EliminarIngesta))

    def _publicar_mensaje_revertir_ingesta(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(ComandoRevertirIngesta))
        publicador.send(mensaje)
        cliente.close()

    def publicar_comando_revertir_ingesta(self, comando, topico):
        payload = ComandoRevertirIngestaPayLoad(
            id_ingesta=str(comando.id_ingesta),
        )

        print(f'publicando comando de compensacion a sta ...')

        comando_integracion = ComandoRevertirIngesta(data=payload)
        self._publicar_mensaje_revertir_ingesta(comando_integracion, topico, AvroSchema(ComandoRevertirIngesta))