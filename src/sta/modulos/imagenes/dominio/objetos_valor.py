"""Objetos valor del dominio de vuelos

En este archivo usted encontrará los objetos valor del dominio de vuelos

"""

from __future__ import annotations

from enum import Enum


class EstadoImagen(str, Enum):
    VERIFICADA = "verificada"
    RECHAZADA = "rechazada"