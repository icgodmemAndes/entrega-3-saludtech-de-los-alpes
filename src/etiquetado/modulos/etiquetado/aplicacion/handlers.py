from etiquetado.seedwork.aplicacion.handlers import Handler
from etiquetado.modulos.etiquetado.infraestructura.despachadores import Despachador


class HandlerEtiquetadoIntegracion(Handler):

    @staticmethod
    def handle_etiquetado_creada(evento):
        print("**********Handler evento***************")
        print(evento)
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-etiquetado')


class HandlerRevertirIntegracion(Handler):

    @staticmethod
    def handle_etiquetado_revertir(evento):
        despachador = Despachador()
        despachador.publicar_comando_revertir_etiquetado(evento, 'comando-revertir-anonimizado')