""" Fábricas para la creación de objetos del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de vuelos

"""

from .entidades import Imagen
from .reglas import URLValida
from .excepciones import TipoObjetoNoExisteEnDominioImagenExcepcion
from sta.seedwork.dominio.repositorios import Mapeador, Repositorio
from sta.seedwork.dominio.fabricas import Fabrica
from sta.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaImagen(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            imagen: Imagen = mapeador.dto_a_entidad(obj)

            self.validar_regla(URLValida(imagen.url_path))

            return imagen

@dataclass
class FabricaImagen(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Imagen.__class__:
            fabrica_imagen = _FabricaImagen()
            return fabrica_imagen.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioImagenExcepcion()

