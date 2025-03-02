from anonimizador.seedwork.dominio.repositorios import Mapeador
from anonimizador.modulos.dominio.entidades import Ingesta
from anonimizador.modulos.dominio.objetos_valor import EstadoIngesta
from .dto import Imagen as ImagenDTO

class MapeadorImagen(Mapeador):

    def obtener_tipo(self) -> type:
        return Ingesta.__class__

    def entidad_a_dto(self, entidad: Ingesta) -> ImagenDTO:
        imagen_dto = ImagenDTO(
            id=str(entidad.id),
            id_ingesta=str(entidad.id_ingesta),
            url_path=entidad.url_path,
            estado=EstadoIngesta.RAW,
        )
        return imagen_dto

    def dto_a_entidad(self, dto: ImagenDTO) -> Ingesta:
        imagen = Ingesta()
        imagen.id_ingesta = dto.id_ingesta
        imagen.url_path = dto.url_path
        imagen.estado = dto.estado

        return imagen