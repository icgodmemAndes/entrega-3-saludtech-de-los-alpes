from pydispatch import dispatcher

from .handlers import HandlerEtiquetadoIntegracion

from etiquetado.modulos.etiquetado.dominio.eventos import EtiquetadoCreada
from etiquetado.modulos.etiquetado.dominio.eventos import EtiquetadoEliminada
from etiquetado.modulos.etiquetado.dominio.eventos import Tagear

dispatcher.connect(HandlerEtiquetadoIntegracion.handle_etiquetado_creada, signal=f'{EtiquetadoCreada.__name__}Integracion')

dispatcher.connect(HandlerEtiquetadoIntegracion.handle_etiquetado_eliminada, signal=f'{EtiquetadoEliminada.__name__}Integracion')

dispatcher.connect(HandlerEtiquetadoIntegracion.handle_tagear, signal=f'{Tagear.__name__}Integracion')