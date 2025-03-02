""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from etiquetado.seedwork.dominio.repositorios import Mapeador
from etiquetado.modulos.dominio.entidades import Imagen, EnriquecerImagen
from etiquetado.modulos.dominio.objetos_valor import EstadoEtiquetado,Modalidad,RegionAnatomica,Patologia,MetadatosImagen,Demografia
from .dto import Imagen as ImagenDTO
from ..dominio.entidades import EnriquecerImagen


class MapeadorImagen(Mapeador):

    def obtener_tipo(self) -> type:
        return Imagen.__class__

    def entidad_a_dto(self, entidad: Imagen) -> ImagenDTO:
        imagen_dto = ImagenDTO(
            id_proveedor=str(entidad.id_ingesta),
            id_paciente=str(entidad.id_paciente),
            url_path=entidad.url_path,
            estado=EstadoEtiquetado.ANONIMIZADA,
            modalidad = entidad.modalidad,
            region= entidad.region_anatomica,
            patologia= entidad.patologia,
            resolucion= entidad.resolucion,
            contraste= entidad.contraste,
            tipo = entidad.tipo,
            fase = entidad.fase,
            grupo_edad=entidad.grupo_edad,
            sexo=entidad.sexo,
            etnicidad=entidad.etnicidad
        )
        return imagen_dto

    def dto_a_entidad(self, dto: ImagenDTO) -> Imagen:
        imagen = Imagen()
        imagen.id_proveedor = dto.id_proveedor
        imagen.id_paciente = dto.id_paciente
        imagen.url_path = dto.url_path
        imagen.estado = dto.estado
        imagen.modalidad =dto.modalidad,
        imagen.region_anatomica = dto.region_anatomica,
        imagen.patologia = dto.patologia,
        imagen.resolucion=dto.resolucion,
        imagen.contraste=dto.contraste,
        imagen.tipo=dto.tipo,
        imagen.fase=dto.fase,
        imagen.grupo_edad=dto.grupo_edad,
        imagen.sexo=dto.sexo,
        imagen.etnicidad=dto.etnicidad

        return imagen