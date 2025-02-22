""" Fábricas para la creación de objetos del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de vuelos

"""

from .entidades import Ingesta
from .reglas import URLValida
from .excepciones import TipoObjetoNoExisteEnDominioIngestaExcepcion
from aeroalpes.seedwork.dominio.repositorios import Mapeador, Repositorio
from aeroalpes.seedwork.dominio.fabricas import Fabrica
from aeroalpes.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaIngesta(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            ingesta: Ingesta = mapeador.dto_a_entidad(obj)

            self.validar_regla(URLValida(ingesta.url_path))

            return ingesta

@dataclass
class FabricaIngesta(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Ingesta.__class__:
            fabrica_ingesta = _FabricaIngesta()
            return fabrica_ingesta.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioIngestaExcepcion()

