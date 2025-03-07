from pydispatch import dispatcher

from .handlers import HandlerEtiquetadoIntegracion,HandlerRevertirIntegracion

from etiquetado.modulos.etiquetado.dominio.eventos import EtiquetadoCreada, Revertir

dispatcher.connect(HandlerEtiquetadoIntegracion.handle_etiquetado_creada, signal=f'{EtiquetadoCreada.__name__}Integracion')

dispatcher.connect(HandlerRevertirIntegracion.handle_etiquetado_revertir, signal=f'{Revertir.__name__}Integracion')