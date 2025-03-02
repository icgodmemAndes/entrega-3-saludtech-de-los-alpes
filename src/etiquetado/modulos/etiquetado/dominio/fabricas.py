""" Fábricas para la creación de objetos del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de vuelos

"""

from .entidades import Etiquetado
from .reglas import URLValida
from .excepciones import TipoObjetoNoExisteEnDominioEtiquetadoExcepcion
from etiquetado.seedwork.dominio.repositorios import Mapeador, Repositorio
from etiquetado.seedwork.dominio.fabricas import Fabrica
from etiquetado.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaEtiquetado(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, list):
            procesados = list()
            for o in obj:
                procesados.append(self._procesar_objeto(o, mapeador))
            return procesados
        else:
            return self._procesar_objeto(obj, mapeador)

    def _procesar_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            etiquetado: Etiquetado = mapeador.dto_a_entidad(obj)

            self.validar_regla(URLValida(etiquetado.url_path))

            return etiquetado

@dataclass
class FabricaEtiquetado(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Etiquetado.__class__:
            fabrica_etiquetado = _FabricaEtiquetado()
            return fabrica_etiquetado.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioEtiquetadoExcepcion()

