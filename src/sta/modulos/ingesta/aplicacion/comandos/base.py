from sta.seedwork.aplicacion.comandos import ComandoHandler
from sta.modulos.ingesta.infraestructura.fabricas import FabricaRepositorio
from sta.modulos.ingesta.dominio.fabricas import FabricaIngesta

class CrearIngestaBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_ingesta: FabricaIngesta = FabricaIngesta()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_ingesta(self):
        return self._fabrica_ingesta
    
class EliminarIngestaBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_ingesta: FabricaIngesta = FabricaIngesta()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_ingesta(self):
        return self._fabrica_ingesta

class RevertirIngestaBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_ingesta: FabricaIngesta = FabricaIngesta()
    
    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_ingesta(self):
        return self._fabrica_ingesta