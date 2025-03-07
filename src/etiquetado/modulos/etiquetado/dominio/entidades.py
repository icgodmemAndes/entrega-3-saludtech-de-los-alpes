"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de etiquetado

"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime

import etiquetado.modulos.etiquetado.dominio.objetos_valor as ov
from etiquetado.modulos.etiquetado.dominio.eventos import EtiquetadoCreada,RevertirEtiquetado
from etiquetado.seedwork.dominio.entidades import AgregacionRaiz, Entidad


@dataclass
class Etiquetado(AgregacionRaiz):
    id_anonimizado: uuid.UUID = field(hash=True, default=None)
    modalidad: str = field(default_factory=str)
    region_anatomica: str = field(default_factory=str)
    patologia: str = field(default_factory=str)
    estado: ov.EstadoEtiquetado = field(default=ov.EstadoEtiquetado.INICIADO)

    def crear_etiquetado(self, etiquetado: Etiquetado):
        self.id_anonimizado = etiquetado.id_anonimizado
        self.modalidad = etiquetado.modalidad
        self.region_anatomica = etiquetado.region_anatomica
        self.patologia = etiquetado.patologia
        print('***** Inicia evento de crear etiquetado ******************')
        if str(etiquetado.id_anonimizado)[-1] in "abcdefghijklmABCDEFGHIJKLM12345":
            print("************ Despacha CrearEtiquetado ********************")
            self.estado: ov.EstadoEtiquetado = field(default=ov.EstadoEtiquetado.INICIADO)
            self.agregar_evento(
            EtiquetadoCreada(id=etiquetado.id, id_anonimizado=self.id_anonimizado, modalidad=self.modalidad,
                             region_anatomica=self.region_anatomica, patologia=self.patologia,
                             fecha_creacion=datetime.now(), estado= self.estado))
        else:
            print("************* Despacha RevertirEtiquetado ****************")
            self.estado: ov.EstadoEtiquetado = field(default=ov.EstadoEtiquetado.RECHAZADO)
            self.agregar_evento(
            RevertirEtiquetado(id=etiquetado.id, id_anonimizado=self.id_anonimizado, modalidad=self.modalidad,
                             region_anatomica=self.region_anatomica, patologia=self.patologia,
                             fecha_creacion=datetime.now(), estado= self.estado))

@dataclass
class Revertir(AgregacionRaiz):
    id_anonimizado: uuid.UUID = field(hash=True, default=None)
    modalidad: str = field(default_factory=str)
    region_anatomica: str = field(default_factory=str)
    patologia: str = field(default_factory=str)

    def revetir_etiquetado(self, revertir: Revertir):
        self.id_anonimizado = revertir.id_anonimizado
        self.modalidad = revertir.modalidad
        self.region_anatomica = revertir.region_anatomica
        self.patologia = revertir.patologia

        self.agregar_evento(
            RevertirEtiquetado(id=revertir.id, id_anonimizado=self.id_anonimizado, modalidad=self.modalidad,
                             region_anatomica=self.region_anatomica, patologia=self.patologia,
                             fecha_creacion=datetime.now()))
