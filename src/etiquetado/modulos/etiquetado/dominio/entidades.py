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
    id_anonimizado: uuid.UUID = field(hash=True, default=None)
    modalidad: str = field(default_factory=str)
    region_anatomica: str = field(default_factory=str)
    patologia: str = field(default_factory=str)
    #estado: ov.EstadoEtiquetado = field(default=ov.EstadoEtiquetado.CREADA)

    def crear_etiquetado(self, etiquetado: Etiquetado):
        self.id_anonimizado = etiquetado.id_anonimizado
        self.modalidad = etiquetado.modalidad
        self.region_anatomica = etiquetado.region_anatomica
        self.patologia = etiquetado.patologia
        #self.estado = etiquetado.estado

        self.agregar_evento(
            EtiquetadoCreada(id=etiquetado.id, id_anonimizado=self.id_anonimizado, modalidad=self.modalidad,
                          region_anatomica=self.region_anatomica,patologia=self.patologia, fecha_creacion=datetime.now()))
    
    def eliminar_etiquetado(self, id_etiquetado: uuid.UUID):
        self.id = id_etiquetado
        self.fecha_eliminacion = datetime.now()
        #self.estado = ov.EstadoEtiquetado.ELIMINADA
        self.agregar_evento(
            EtiquetadoEliminada(id=self.id, estado=self.estado, fecha_eliminacion=self.fecha_eliminacion)
            )

        return self.id
