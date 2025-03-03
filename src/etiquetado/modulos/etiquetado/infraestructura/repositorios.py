""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""
from datetime import datetime
from uuid import UUID

from etiquetado.config.db import db
from etiquetado.modulos.etiquetado.dominio.entidades import Etiquetado
from etiquetado.modulos.etiquetado.dominio.fabricas import FabricaEtiquetado
from .mapeadores import MapeadorEtiquetado
from etiquetado.modulos.etiquetado.dominio.repositorios import RepositorioEtiquetado
from .dto import Etiquetado as EtiquetadoDTO


class RepositorioEtiquetadoSQLite(RepositorioEtiquetado):

    def __init__(self):
        self._fabrica_etiquetado: FabricaEtiquetado = FabricaEtiquetado()

    @property
    def fabrica_etiquetado(self):
        return self._fabrica_etiquetado

    def agregar(self, etiquetado: Etiquetado):
        etiquetado.fecha_creacion = datetime.now()
        etiquetado_dto = self.fabrica_etiquetado.crear_objeto(etiquetado, MapeadorEtiquetado())
        db.session.add(etiquetado_dto)
        print('AGREGAR etiquetado completo')

    def obtener_por_id(self, id: UUID) -> Etiquetado:
        etiquetado_dto = db.session.query(EtiquetadoDTO).filter_by(id=str(id)).one()
        return self.fabrica_etiquetado.crear_objeto(etiquetado_dto, MapeadorEtiquetado())

    def obtener_todos(self) -> list[Etiquetado]:
        etiquetados_dto = db.session.query(EtiquetadoDTO).all()
        etiquetados = list()

        for etiquetado_dto in etiquetados_dto:
            etiquetados.append(self.fabrica_etiquetado.crear_objeto(etiquetado_dto, MapeadorEtiquetado()))

        return etiquetados

    def actualizar(self, etiquetado: Etiquetado):
        # TODO
        raise NotImplementedError

    def eliminar(self, etiquetado_id: UUID):
        etiquetado = db.session.query(EtiquetadoDTO).filter_by(id=str(etiquetado_id)).one()

        if etiquetado is None:
            raise Exception('Etiquetado no encontrada')
        
        etiquetado.fecha_eliminacion = datetime.now()

        db.session.update(etiquetado)
        db.session.commit()
        print('ELIMINAR etiquetado completo')
