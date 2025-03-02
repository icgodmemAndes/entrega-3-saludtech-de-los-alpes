""" Fábricas para la creación de objetos del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de vuelos

"""

from .entidades import Imagen, EnriquecerImagen
from .reglas import URLValida
from .excepciones import TipoObjetoNoExisteEnDominioImagenExcepcion
from etiquetado.seedwork.dominio.repositorios import Mapeador, Repositorio
from etiquetado.seedwork.dominio.fabricas import Fabrica
from etiquetado.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaImagen(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            print('******Mapea entidad a dto***********')
            return mapeador.entidad_a_dto(obj)
        else:
            imagen: Imagen = mapeador.dto_a_entidad(obj)
            print('******Mapea dto a Entidad***********')
            print(imagen.url_path)
            #self.validar_regla(URLValida(imagen.url_path))
            print('******print valida regla***********')
            return imagen

@dataclass
class FabricaImagen(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Imagen.__class__:
            fabrica_imagen = _FabricaImagen()
            return fabrica_imagen.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioImagenExcepcion()

