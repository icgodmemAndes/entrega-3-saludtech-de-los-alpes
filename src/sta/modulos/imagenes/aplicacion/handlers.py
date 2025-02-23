from sta.seedwork.aplicacion.handlers import Handler
from sta.modulos.imagenes.infraestructura.despachadores import Despachador

class HandlerImagenIntegracion(Handler):

    @staticmethod
    def handle_imagen_procesada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-imagen')