""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de vuelos

"""

from dataclasses import dataclass, field
from etiquetado.seedwork.dominio.fabricas import Fabrica
from etiquetado.seedwork.dominio.repositorios import Repositorio
from etiquetado.modulos.dominio.repositorios import RepositorioImagen

from .repositorios import RepositorioImagenMySQL
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioImagen.__class__:
            return RepositorioImagenMySQL()
        else:
            raise ExcepcionFabrica()