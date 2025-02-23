from pydispatch import dispatcher

from .handlers import HandlerIngestaIntegracion

from sta.modulos.ingesta.dominio.eventos import IngestaCreada

dispatcher.connect(HandlerIngestaIntegracion.handle_ingesta_creada, signal=f'{IngestaCreada.__name__}Integracion')