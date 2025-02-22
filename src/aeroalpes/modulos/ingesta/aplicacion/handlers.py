from aeroalpes.modulos.ingesta.dominio.eventos import IngestaCreada
from aeroalpes.seedwork.aplicacion.handlers import Handler
from aeroalpes.modulos.ingesta.infraestructura.despachadores import Despachador

class HandlerIngestaIntegracion(Handler):

    @staticmethod
    def handle_ingesta_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-ingesta')