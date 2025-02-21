from aeroalpes.seedwork.aplicacion.comandos import ComandoHandler
from aeroalpes.modulos.ingesta.infraestructura.fabricas import FabricaRepositorio
from aeroalpes.modulos.ingesta.dominio.fabricas import FabricaIngesta

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
    