from dataclasses import dataclass
from anonimizador.seedwork.dominio.fabricas import Fabrica
from anonimizador.seedwork.dominio.repositorios import Repositorio
from anonimizador.modulos.dominio.repositorios import RepositorioImagen

from .repositorios import RepositorioImagenAnonimizadaMySQL
from .excepciones import ExcepcionFabrica


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioImagen.__class__:
            return RepositorioImagenAnonimizadaMySQL()
        else:
            raise ExcepcionFabrica()
