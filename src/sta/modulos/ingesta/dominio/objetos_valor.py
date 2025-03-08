"""Objetos valor del dominio de vuelos

En este archivo usted encontrará los objetos valor del dominio de vuelos

"""

from __future__ import annotations

from enum import Enum


class EstadoIngesta(str, Enum):
    CREADA = "Creada"
    PENDIENTE = "Pendiente"
    RECHAZADO = "Rechazada"
    FINALIZADA = "Finalizada"
    ELIMINADA = "Eliminada"
    FALLIDA = "Fallida"
    ALERTADA = "Alertada"