from etiquetado.seedwork.aplicacion.comandos import ComandoHandler
from etiquetado.modulos.etiquetado.infraestructura.fabricas import FabricaRepositorio
from etiquetado.modulos.etiquetado.dominio.fabricas import FabricaEtiquetado, FabricaTagear

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
    
class EliminarEtiquetadoBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_etiquetado: FabricaEtiquetado = FabricaEtiquetado()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_etiquetado(self):
        return self._fabrica_etiquetado


class TagearBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_tagear: FabricaTagear = FabricaTagear()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

    @property
    def fabrica_tagear(self):
        return self._fabrica_Tagear