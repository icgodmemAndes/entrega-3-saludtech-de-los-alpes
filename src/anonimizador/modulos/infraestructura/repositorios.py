from uuid import UUID
from datetime import datetime
import base64

from anonimizador.config.db import session
from anonimizador.config.db import Base as db
from anonimizador.modulos.dominio.entidades import Ingesta
from anonimizador.modulos.dominio.fabricas import FabricaImagen  # type: ignore
from anonimizador.modulos.dominio.repositorios import RepositorioImagen
from .mapeadores import MapeadorImagen

class RepositorioImagenAnonimizadaMySQL(RepositorioImagen):


    def __init__(self):
        self._session = session
        self._fabrica_imagen: FabricaImagen = FabricaImagen()

    @property
    def fabrica_imagen(self):
        return self._fabrica_imagen

    def agregar(self, ingesta: Ingesta):
        print('LLama agregar')
        ingesta.fecha_creacion = datetime.now()
        ingesta.url_path = self.ofuscar_url(ingesta.url_path)        

        imagen_dto = self.fabrica_imagen.crear_objeto(ingesta, MapeadorImagen())        

        self._session.add(imagen_dto)
        self._session.commit()
        print(f"#added agregar() {ingesta.__dict__}")

    def obtener_por_id(self, id: UUID) -> Ingesta:
        raise NotImplementedError

    def obtener_todos(self) -> list[Ingesta]:
        raise NotImplementedError

    def actualizar(self, imagen: Ingesta):
        raise NotImplementedError

    def eliminar(self, imagen: Ingesta):
        raise NotImplementedError

    def ofuscar_url(self, url_path: str) -> str:
        bytes_url = url_path.encode('utf-8')
        base64_bytes = base64.b64encode(bytes_url)
        return base64_bytes.decode('utf-8')