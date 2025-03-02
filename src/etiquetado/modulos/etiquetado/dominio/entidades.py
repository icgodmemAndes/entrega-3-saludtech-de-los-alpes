"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de etiquetado

"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime

import etiquetado.modulos.etiquetado.dominio.objetos_valor as ov
from etiquetado.modulos.etiquetado.dominio.eventos import EtiquetadoCreada, EtiquetadoEliminada
from etiquetado.seedwork.dominio.entidades import AgregacionRaiz, Entidad


@dataclass
class Proveedor(Entidad):
    id_provider: uuid.UUID = field(hash=True, default=None)


@dataclass
class Paciente(Entidad):
    full_name: str = field(default_factory=str)
    id_patient: uuid.UUID = field(hash=True, default=None)


@dataclass
class Etiquetado(AgregacionRaiz):
    id_proveedor: uuid.UUID = field(hash=True, default=None)
    id_paciente: uuid.UUID = field(hash=True, default=None)
    url_path: str = field(default_factory=str)
    estado: ov.EstadoEtiquetado = field(default=ov.EstadoEtiquetado.CREADA)

    def crear_etiquetado(self, etiquetado: Etiquetado):
        self.id_proveedor = etiquetado.id_proveedor
        self.id_paciente = etiquetado.id_paciente
        self.url_path = etiquetado.url_path
        self.estado = etiquetado.estado

        self.agregar_evento(
            EtiquetadoCreada(id=etiquetado.id, id_proveedor=self.id_proveedor, id_paciente=self.id_paciente,
                          url_path=self.url_path, estado=self.estado, fecha_creacion=datetime.now()))
    
    def eliminar_etiquetado(self, id_etiquetado: uuid.UUID):
        self.id = id_etiquetado
        self.fecha_eliminacion = datetime.now()
        self.estado = ov.EstadoEtiquetado.ELIMINADA
        self.agregar_evento(
            EtiquetadoEliminada(id=self.id, estado=self.estado, fecha_eliminacion=self.fecha_eliminacion)
            )

        return self.id
