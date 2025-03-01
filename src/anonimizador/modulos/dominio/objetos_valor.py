"""Objetos valor del dominio de anonimizador

En este archivo usted encontrará los objetos valor del dominio de anonimizador

"""

from enum import Enum

class EstadoImagen(str, Enum):
    RAW = "RAW"
    ANONIMIZADA = "ANONIMIZADA"
