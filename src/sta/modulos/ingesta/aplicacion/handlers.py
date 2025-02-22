from sta.seedwork.aplicacion.handlers import Handler
from sta.modulos.ingesta.infraestructura.despachadores import Despachador

class HandlerIngestaIntegracion(Handler):

    @staticmethod
    def handle_ingesta_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-ingesta')