
from uuid import UUID
from datetime import datetime

from anonimizador.config.db import db
from anonimizador.modulos.dominio.entidades import Ingesta
from anonimizador.modulos.dominio.fabricas import FabricaImagen  # type: ignore
from .mapeadores import MapeadorImagen
from anonimizador.modulos.dominio.repositorios import RepositorioImagen
import base64


class RepositorioImagenAnonimizadaMySQL(RepositorioImagen):

    def __init__(self):
        self._fabrica_imagen: FabricaImagen = FabricaImagen()

    @property
    def fabrica_imagen(self):
        return self._fabrica_imagen

    def agregar(self, imagen: Ingesta):
        imagen.fecha_creacion = datetime.now()
        #Se ofusca la url de la imagen
        imagen.url_path = self.ofuscar_url(imagen.url_path)
        imagen_dto = self.fabrica_imagen.crear_objeto(imagen, MapeadorImagen())
        db.session.add(imagen_dto)

    def obtener_por_id(self, id: UUID) -> Ingesta:
        # id is not accessed
        raise NotImplementedError

    def obtener_todos(self) -> list[Ingesta]:
        # TODO
        raise NotImplementedError
    def actualizar(self, imagen: Ingesta):
        # imagen is not accesse
        raise NotImplementedError

    def eliminar(self, imagen: Ingesta):
        # imagen is not accessed
        raise NotImplementedError
    
    def ofuscar_url(self, url_path: str):

        bytes_url = url_path.encode('utf-8')
        base64_bytes = base64.b64encode(bytes_url)
        # Convert back to string and return
        return base64_bytes.decode('utf-8')
