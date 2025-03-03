from etiquetado.seedwork.aplicacion.comandos import ComandoHandler
from etiquetado.modulos.etiquetado.infraestructura.fabricas import FabricaRepositorio
from etiquetado.modulos.etiquetado.dominio.fabricas import FabricaEtiquetado

class CrearEtiquetadoBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_etiquetado: FabricaEtiquetado = FabricaEtiquetado()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_etiquetado(self):
        return self._fabrica_etiquetado
