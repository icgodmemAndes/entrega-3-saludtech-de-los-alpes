"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de ingesta

"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

import sta.modulos.ingesta.dominio.objetos_valor as ov
from sta.modulos.ingesta.dominio.eventos import IngestaCreada

from sta.seedwork.dominio.entidades import AgregacionRaiz, Entidad

@dataclass
class Proveedor(Entidad):
    id_provider: uuid.UUID = field(hash=True, default=None)

@dataclass
class Paciente(Entidad):
    full_name: str = field(default_factory=str)
    id_patient: uuid.UUID = field(hash=True, default=None)


@dataclass
class Ingesta(AgregacionRaiz):
    id_proveedor : uuid.UUID = field(hash=True, default=None)
    id_paciente : uuid.UUID = field(hash=True, default=None)
    url_path: str = field(default_factory=str)
    estado: ov.EstadoIngesta = field(default=ov.EstadoIngesta.CREADA)

    def crear_ingesta(self, ingesta: Ingesta):
        self.id_proveedor = ingesta.id_proveedor
        self.id_paciente = ingesta.id_paciente
        self.url_path = ingesta.url_path
        self.estado = ingesta.estado

        self.agregar_evento(IngestaCreada(id_proveedor=self.id_proveedor, id_paciente=self.id_paciente, url_path = self.url_path,estado=self.estado, fecha_creacion=self.fecha_creacion))