from uuid import UUID

from etiquetado.modulos.dominio.entidades import Imagen
from etiquetado.modulos.dominio.repositorios import RepositorioImagen

class RepositorioImagenSQLAlchemy(RepositorioImagen):

    def __init__(self):
        self._fabrica_imagen: FabricaImagen = FabricaImagen()

    @property
    def fabrica_imagen(self):
        return self._fabrica_imagen

    def obtener_por_id(self, id: UUID) -> Imagen:
        imagen_dto = db.session.query(ImagenDTO).filter_by(id=str(id)).one()
        return self._fabrica_imagen.crear_objeto(imagen_dto, MapeadorImagen())

    def obtener_todos(self) -> list[Imagen]:
        # TODO
        raise NotImplementedError

    def agregar(self, imagen: Imagen):
        imagen_dto = self.fabrica_imagen.crear_objeto(imagen, MapeadorImagen())

        db.session.add(imagen_dto)

    def actualizar(self, imagen: Imagen):
        # TODO
        raise NotImplementedError

    def eliminar(self, imagen_id: UUID):
        # TODO
        raise NotImplementedError