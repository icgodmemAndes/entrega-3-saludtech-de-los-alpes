import pulsar
from pulsar.schema import *

from anonimizador.seedwork.infraestructura import utils

class Despachador:
    def __init__(self):
        self.client = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        self.producers = {}

    def publicar_mensaje(self, mensaje, topico):
        if topico not in self.producers:
            self.producers[topico] = self.client.create_producer(
                topico, 
                schema=AvroSchema(mensaje.__class__)
            )
        
        self.producers[topico].send(mensaje)
    
    def __del__(self):
        self.close()
        
    def close(self):
        for producer in self.producers.values():
            producer.close()
        self.client.close()
