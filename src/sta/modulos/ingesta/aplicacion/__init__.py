from pydispatch import dispatcher

from .handlers import HandlerIngestaIntegracion

from sta.modulos.ingesta.dominio.eventos import IngestaCreada
from sta.modulos.ingesta.dominio.eventos import IngestaEliminada

dispatcher.connect(HandlerIngestaIntegracion.handle_ingesta_creada, signal=f'{IngestaCreada.__name__}Integracion')

dispatcher.connect(HandlerIngestaIntegracion.handle_ingesta_eliminada, signal=f'{IngestaEliminada.__name__}Integracion')