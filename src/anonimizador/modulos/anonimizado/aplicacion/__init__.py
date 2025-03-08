from pydispatch import dispatcher

from .handlers import HandlerAnonimizadoIntegracion

from anonimizador.modulos.anonimizado.dominio.eventos import AnonimizadoProcesada
from anonimizador.modulos.anonimizado.dominio.eventos import AnonimizadoRevertido

dispatcher.connect(HandlerAnonimizadoIntegracion.handle_anonimizado_procesada, signal=f'{AnonimizadoProcesada.__name__}Integracion')
dispatcher.connect(HandlerAnonimizadoIntegracion.handle_anonimizado_revertida, signal=f'{AnonimizadoRevertido.__name__}Integracion')

