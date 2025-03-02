""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from etiquetado.seedwork.dominio.repositorios import Mapeador
from etiquetado.modulos.dominio.entidades import Imagen
from etiquetado.modulos.dominio.objetos_valor import EstadoEtiquetado
from .dto import Imagen as ImagenDTO

class MapeadorImagen(Mapeador):

    def obtener_tipo(self) -> type:
        return Imagen.__class__

    def entidad_a_dto(self, entidad: Imagen) -> ImagenDTO:
        imagen_dto = ImagenDTO(
            id=str(entidad.id),
            id_proveedor=str(entidad.id_ingesta),
            id_paciente=str(entidad.id_paciente),
            url_path=entidad.url_path,
            estado=EstadoEtiquetado.ANONIMIZADA,
        )
        return imagen_dto

    def dto_a_entidad(self, dto: ImagenDTO) -> Imagen:
        imagen = Imagen()
        imagen.id_proveedor = dto.id_proveedor
        imagen.id_paciente = dto.id_paciente
        imagen.url_path = dto.url_path
        imagen.estado = dto.estado

        return imagen