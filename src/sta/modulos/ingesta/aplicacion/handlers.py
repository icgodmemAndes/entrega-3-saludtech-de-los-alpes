from sta.seedwork.aplicacion.handlers import Handler
from sta.modulos.ingesta.infraestructura.despachadores import Despachador

class HandlerIngestaIntegracion(Handler):

    @staticmethod
    def handle_ingesta_procesada(evento):
        despachador = Despachador()
        despachador.publicar_comando_iniciar_anonimizado(evento, 'comando-iniciar-anonimizado')
        despachador.publicar_evento_ingesta_creada(evento, 'evento-ingesta-creada')
    
    @staticmethod
    def handle_ingesta_eliminada(evento):
        despachador = Despachador()
        despachador.publicar_evento_ingesta_eliminada(evento, 'evento-ingesta-eliminada')
    
    @staticmethod
    def handle_ingesta_revertida(evento):
        despachador = Despachador()
        despachador.publicar_evento_ingesta_revertida(evento, 'evento-fallo-ingesta')