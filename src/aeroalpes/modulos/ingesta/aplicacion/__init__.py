from pydispatch import dispatcher

from .handlers import HandlerIngestaIntegracion

from aeroalpes.modulos.ingesta.dominio.eventos import IngestaCreada, IngestaFinalizada, IngestaRechazada

dispatcher.connect(HandlerIngestaIntegracion.handle_ingesta_creada, signal=f'{IngestaCreada.__name__}Integracion')
dispatcher.connect(HandlerIngestaIntegracion.handle_ingesta_finalizada, signal=f'{IngestaFinalizada.__name__}Integracion')
dispatcher.connect(HandlerIngestaIntegracion.handle_ingesta_rechazada, signal=f'{IngestaRechazada.__name__}Integracion')