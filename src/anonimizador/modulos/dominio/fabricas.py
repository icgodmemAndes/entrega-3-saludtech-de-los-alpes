""" Fábricas para la creación de objetos del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de vuelos

"""

from .entidades import Ingesta
from anonimizador.seedwork.dominio.repositorios import Mapeador, Repositorio
from anonimizador.seedwork.dominio.fabricas import Fabrica
from anonimizador.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass
from anonimizador.modulos.dominio.excepciones import TipoObjetoNoExisteEnDominioImagenExcepcion

@dataclass
class _FabricaImagen(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            imagen: Ingesta = mapeador.dto_a_entidad(obj)
            return imagen

@dataclass
class FabricaImagen(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Ingesta.__class__:
            fabrica_imagen = _FabricaImagen()
            return fabrica_imagen.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioImagenExcepcion()

