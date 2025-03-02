

from etiquetado.seedwork.aplicacion.handlers import Handler
from etiquetado.modulos.infraestructura.despachadores import Despachador

class HandlerImagenDominio(Handler):

    @staticmethod
    def handle_imagen_tageada(evento):
        print('================ IMAGEN TAGEADA ===========')
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-imagen')

    @staticmethod
    def handle_enriquecer(evento):
        print('================ ENRIQUECER ===========')
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-ingesta')