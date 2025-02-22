from aeroalpes.modulos.ingesta.dominio.eventos import IngestaCreada, IngestaFinalizada, IngestaRechazada
from aeroalpes.seedwork.aplicacion.handlers import Handler
from aeroalpes.modulos.ingesta.infraestructura.despachadores import Despachador

class HandlerIngestaIntegracion(Handler):

    @staticmethod
    def handle_ingesta_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')

    @staticmethod
    def handle_ingesta_rechazada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')

    @staticmethod
    def handle_ingesta_finalizada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')   