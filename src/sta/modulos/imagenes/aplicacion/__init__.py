from pydispatch import dispatcher

from .handlers import HandlerImagenIntegracion

from sta.modulos.imagenes.dominio.eventos import ImagenProcesada

dispatcher.connect(HandlerImagenIntegracion.handle_imagen_procesada, signal=f'{ImagenProcesada.__name__}Integracion')