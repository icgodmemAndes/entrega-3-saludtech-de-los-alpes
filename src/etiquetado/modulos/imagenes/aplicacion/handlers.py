from etiquetado.seedwork.aplicacion.handlers import Handler
from etiquetado.modulos.imagenes.infraestructura.despachadores import Despachador

class HandlerImagenIntegracion(Handler):

    @staticmethod
    def handle_imagen_procesada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-imagen')