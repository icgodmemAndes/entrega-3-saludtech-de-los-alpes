"""Entidades del dominio de cliente

En este archivo usted encontrará las entidades del dominio de cliente

"""
import uuid
from etiquetado.seedwork.dominio.entidades import Entidad, AgregacionRaiz
from dataclasses import dataclass, field

from .objetos_valor import Modalidad, RegionAnatomica, Patologia, MetadatosImagen, Demografia, EstadoEtiquetado

@dataclass
class Proveedor(Entidad):
    id_provider: uuid.UUID = field(hash=True, default=None)


@dataclass
class Paciente(Entidad):
    full_name: str = field(default_factory=str)
    id_patient: uuid.UUID = field(hash=True, default=None)


@dataclass
class Imagen(AgregacionRaiz):
    id_proveedor: uuid.UUID = field(hash=True, default=None)
    id_paciente: uuid.UUID = field(hash=True, default=None)
    url_path: str = field(default_factory=str)
    estado: EstadoEtiquetado = field(default=EstadoEtiquetado.CREADA)
    modalidad: Modalidad = field(default_factory=Modalidad)
    region: RegionAnatomica = field(default_factory=RegionAnatomica)
    patologia: Patologia = field(default_factory=Patologia)
    metadatos: MetadatosImagen = field(default_factory=MetadatosImagen)
    demografia: Demografia  = field(default_factory=Demografia)

    #def tagear_imagen(self, imagen):
    #    self.id_ingesta = imagen.id_ingesta
    #    self.url_path = imagen.url_path
    #    self.estado = imagen.estado

    #    self.agregar_comando(
    #        ImagenProcesada(id_imagen=imagen.id, id_ingesta=self.id_ingesta, url_path=self.url_path,
    #                        estado=self.estado))

@dataclass
class Dato(AgregacionRaiz):
    id_proveedor: uuid.UUID = field(hash=True, default=None)
    id_paciente: uuid.UUID = field(hash=True, default=None)
    url_path: str = field(default_factory=str)
    estado: EstadoEtiquetado = field(default=EstadoEtiquetado.FINALIZADA)
    etiquetas: list[str] = field(default_factory=list[str])
    modelo_utilizado: str = field(default_factory=str)
    confianza: float = field(default_factory=float)

@dataclass
class ImagenTageada(Entidad, AgregacionRaiz):
    id_proveedor: uuid.UUID = field(hash=True, default=None)
    id_paciente: uuid.UUID = field(hash=True, default=None)
    url_path: str = field(default_factory=str)
    estado: EstadoEtiquetado = field(default=EstadoEtiquetado.CREADA)
    etiquetas: list[str] = field(default_factory=list[str])
    modelo_utilizado: str = field(default_factory=str)
    confianza: float = field(default_factory=float)