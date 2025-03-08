from anonimizador.seedwork.aplicacion.handlers import Handler
from anonimizador.modulos.anonimizado.infraestructura.despachadores import Despachador

class HandlerAnonimizadoIntegracion(Handler):

    @staticmethod
    def handle_anonimizado_procesada(evento):
        despachadorIniciarEtiquetado = Despachador()
        despachadorIniciarEtiquetado.publicar_comando_iniciar_etiquetado(evento, 'comando-crear-etiquetado')

        despachadorEliminarIngesta = Despachador()
        despachadorEliminarIngesta.publicar_comando_eliminar_ingesta(evento, 'comando-eliminar-ingesta')
    
    @staticmethod
    def handle_anonimizado_revertida(evento):
        despachadorRevertirIngesta = Despachador()
        despachadorRevertirIngesta.publicar_comando_revertir_ingesta(evento, 'comando-revertir-ingesta')