from .entidades import Anonimizado
from .excepciones import TipoObjetoNoExisteEnDominioAnonimizadoExcepcion
from anonimizador.seedwork.dominio.repositorios import Mapeador, Repositorio
from anonimizador.seedwork.dominio.fabricas import Fabrica
from anonimizador.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaAnonimizado(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            anonimizado: Anonimizado = mapeador.dto_a_entidad(obj)
            return anonimizado

@dataclass
class FabricaAnonimizado(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Anonimizado.__class__:
            fabrica_anonimizado = _FabricaAnonimizado()
            return fabrica_anonimizado.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioAnonimizadoExcepcion()

