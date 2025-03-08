""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""
from uuid import UUID
from datetime import datetime

from sta.config.db import db
from sta.modulos.imagenes.dominio.entidades import Imagen
from sta.modulos.imagenes.dominio.fabricas import FabricaImagen
from .mapeadores import MapeadorImagen
from sta.modulos.imagenes.dominio.repositorios import RepositorioImagen


class RepositorioImagenSQLite(RepositorioImagen):

    def __init__(self):
        self._fabrica_imagen: FabricaImagen = FabricaImagen()

    @property
    def fabrica_imagen(self):
        return self._fabrica_imagen

    def agregar(self, imagen: Imagen):
        imagen.fecha_creacion = datetime.now()
        imagen_dto = self.fabrica_imagen.crear_objeto(imagen, MapeadorImagen())
        db.session.add(imagen_dto)
    
    def obtener_por_id_ingesta(self, id_ingesta: UUID) -> Imagen:
        imagen_dto = db.session.query(Imagen).filter(Imagen.id_ingesta == str(id_ingesta)).one()
        
        return self.fabrica_imagen.crear_objeto(imagen_dto, MapeadorImagen())
    
    def revertir(self, id_ingesta: UUID):
        imagen = db.session.query(Imagen).filter(Imagen.id_ingesta == str(id_ingesta)).one()
        
        if imagen is None:
            raise Exception('Imagen no encontrada')
        
        imagen.estado = 'RECHAZADA'
        imagen.fecha_eliminacion = datetime.now()
        print(f'RECHAZAR completo imagen id_ingesta: {id_ingesta}')


    def obtener_por_id(self, id: UUID) -> Imagen:
        raise NotImplementedError

    def obtener_todos(self) -> list[Imagen]:
        # TODO
        raise NotImplementedError

    def actualizar(self, imagen: Imagen):
        # TODO
        raise NotImplementedError

    def eliminar(self, imagen_id: UUID):
        # TODO
        raise NotImplementedError

    def eliminar_entidad(self, imagen: Imagen):
        raise NotImplementedError

    def revertir_entidad(self, imagen: Imagen):
        raise NotImplementedError