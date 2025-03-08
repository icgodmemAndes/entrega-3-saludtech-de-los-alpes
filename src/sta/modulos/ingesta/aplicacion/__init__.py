from pydispatch import dispatcher

from .handlers import HandlerIngestaIntegracion

from sta.modulos.ingesta.dominio.eventos import IniciarAnonimizado
from sta.modulos.ingesta.dominio.eventos import IngestaEliminada
from sta.modulos.ingesta.dominio.eventos import IngestaRevertida
from sta.modulos.ingesta.dominio.eventos import IngestaAlertada

dispatcher.connect(HandlerIngestaIntegracion.handle_ingesta_procesada, signal=f'{IniciarAnonimizado.__name__}Integracion')

dispatcher.connect(HandlerIngestaIntegracion.handle_ingesta_eliminada, signal=f'{IngestaEliminada.__name__}Integracion')

dispatcher.connect(HandlerIngestaIntegracion.handle_ingesta_revertida, signal=f'{IngestaRevertida.__name__}Integracion')

dispatcher.connect(HandlerIngestaIntegracion.handle_ingesta_alertada, signal=f'{IngestaAlertada.__name__}Integracion')