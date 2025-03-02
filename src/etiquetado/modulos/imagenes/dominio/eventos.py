from __future__ import annotations

import uuid
from dataclasses import dataclass
from etiquetado.seedwork.dominio.eventos import (EventoDominio)


@dataclass
class ImagenProcesada(EventoDominio):
    id_imagen: uuid.UUID = None
    id_etiquetado: uuid.UUID = None
    url_path: str = None
    estado: str = None
