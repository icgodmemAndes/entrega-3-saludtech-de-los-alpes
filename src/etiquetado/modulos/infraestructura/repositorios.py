import base64
from datetime import datetime
from uuid import UUID

from etiquetado.modulos.dominio.entidades import Imagen
from etiquetado.modulos.dominio.fabricas import FabricaImagen  # type: ignore
from .mapeadores import MapeadorImagen
from etiquetado.modulos.dominio.repositorios import RepositorioImagen

from etiquetado.config.db import db


class RepositorioImagenMySQL(RepositorioImagen):

    def __init__(self):
        self._fabrica_imagen: FabricaImagen = FabricaImagen()

    @property
    def fabrica_imagen(self):
        return self._fabrica_imagen

    def obtener_por_id(self, id: UUID) -> Imagen:
        # id is not accessed
        raise NotImplementedError

    def obtener_todos(self) -> list[Imagen]:
        # TODO
        raise NotImplementedError

    def agregar(self, imagen: Imagen):
        imagen.fecha_creacion = datetime.now()
        # Se ofusca la url de la imagen
        imagen.url_path = self.ofuscar_url(imagen.url_path)
        imagen_dto = self.fabrica_imagen.crear_objeto(imagen, MapeadorImagen())
        db.session.add(imagen_dto)

    def actualizar(self, imagen: Imagen):
        # TODO
        raise NotImplementedError

    def eliminar(self, imagen_id: UUID):
        # TODO
        raise NotImplementedError

    def ofuscar_url(self, url_path: str):

        bytes_url = url_path.encode('utf-8')
        base64_bytes = base64.b64encode(bytes_url)
        # Convert back to string and return
        return base64_bytes.decode('utf-8')