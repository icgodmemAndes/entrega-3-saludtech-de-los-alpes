from etiquetado.seedwork.aplicacion.handlers import Handler
from etiquetado.modulos.etiquetado.infraestructura.despachadores import Despachador

class HandlerEtiquetadoIntegracion(Handler):

    @staticmethod
    def handle_etiquetado_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-etiquetado')
    
    @staticmethod
    def handle_etiquetado_eliminada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-etiquetado')