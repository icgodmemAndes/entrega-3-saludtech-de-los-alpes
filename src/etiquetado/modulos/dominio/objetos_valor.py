"""Objetos valor del dominio de cliente

En este archivo usted encontrará los objetos valor del dominio de cliente

"""

from etiquetado.seedwork.dominio.objetos_valor import ObjetoValor
from dataclasses import dataclass
from enum import Enum


# 📌 Modalidad de imagen (Rayos X, Ultrasonido, etc.)
@dataclass(frozen=True)
class Modalidad(ObjetoValor):
    nombre: str  # Ej: "Rayos X", "Resonancia Magnética"

# 📌 Región Anatómica (Cabeza, Tórax, etc.)
@dataclass(frozen=True)
class RegionAnatomica(ObjetoValor):
    nombre: str  # Ej: "Cerebro", "Pulmones"

# 📌 Patología o condición médica (Neumonía, fractura, etc.)
@dataclass(frozen=True)
class Patologia(ObjetoValor):
    nombre: str  # Ej: "Neumonía", "Fractura", "Tumor"

# 📌 Metadatos de la imagen
@dataclass(frozen=True)
class MetadatosImagen(ObjetoValor):
    resolucion: str  # Ej: "1920x1080"
    contraste: str  # Ej: "Alto", "Medio", "Bajo"
    tipo: str  # Ej: "2D", "3D"
    fase: str  # Ej: "Pre-tratamiento", "Post-tratamiento".


# 📌 Demografía del paciente (usado en el entrenamiento de IA)
@dataclass(frozen=True)
class Demografia(ObjetoValor):
    grupo_edad: str  # Ej: "Adulto", "Pediátrico"
    sexo: str  # Ej: "Masculino", "Femenino"
    etnicidad: str  # Ej: "Latino", "Caucásico"


class EstadoEtiquetado(str, Enum):
    CREADA = "Creada"
    PENDIENTE = "Pendiente"
    RECHAZADO = "Rechazada"
    FINALIZADA = "Finalizada"
    RAW = "RAW"
    ANONIMIZADA = "ANONIMIZADA"