from dataclasses import dataclass
from anonimizador.seedwork.dominio.fabricas import Fabrica
from anonimizador.seedwork.dominio.repositorios import Repositorio
from anonimizador.modulos.anonimizado.dominio.repositorios import RepositorioAnonimizado

from .repositorios import RepositorioAnonimizadoSQLite
from .excepciones import ExcepcionFabrica


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioAnonimizado.__class__:
            return RepositorioAnonimizadoSQLite()
        else:
            raise ExcepcionFabrica()
