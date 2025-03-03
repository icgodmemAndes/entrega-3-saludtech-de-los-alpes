from pydispatch import dispatcher

from .handlers import HandlerEtiquetadoIntegracion

from etiquetado.modulos.etiquetado.dominio.eventos import EtiquetadoCreada

dispatcher.connect(HandlerEtiquetadoIntegracion.handle_etiquetado_creada, signal=f'{EtiquetadoCreada.__name__}Integracion')