from enum import Enum

class TipoImagen(Enum):
    cabeza = 1
    torso = 2
    extremidades = 3

from enum import Enum

class TipoCliente(Enum):
    natural = 1
    corporativo = 2

class EstadoEtiquetado(str, Enum):
    CREADA = "Creada"
    PENDIENTE = "Pendiente"
    RECHAZADO = "Rechazada"
    FINALIZADA = "Finalizada"