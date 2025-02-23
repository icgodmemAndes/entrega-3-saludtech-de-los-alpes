""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

import random
from sta.seedwork.dominio.repositorios import Mapeador
from sta.modulos.imagenes.dominio.entidades import Imagen
from sta.modulos.imagenes.dominio.objetos_valor import EstadoImagen
from .dto import Imagen as ImagenDTO

class MapeadorImagen(Mapeador):

    def obtener_tipo(self) -> type:
        return Imagen.__class__

    def entidad_a_dto(self, entidad: Imagen) -> ImagenDTO:
        imagen_dto = ImagenDTO(
            id=str(entidad.id),
            id_ingesta=str(entidad.id_ingesta),
            url_path=entidad.url_path,
            estado=random.choice(list(EstadoImagen)),
        )
        return imagen_dto

    def dto_a_entidad(self, dto: ImagenDTO) -> Imagen:
        imagen = Imagen()
        imagen.id_ingesta = dto.id_ingesta
        imagen.url_path = dto.url_path
        imagen.estado = dto.estado

        return imagen