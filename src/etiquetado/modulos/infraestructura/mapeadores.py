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

    def entidad_a_dto(self, entidad: EnriquecerImagen) -> ImagenDTO:
        imagen_dto = ImagenDTO(
            id_proveedor=str(entidad.id_ingesta),
            id_paciente=str(entidad.id_paciente),
            url_path=entidad.url_path,
            estado=EstadoEtiquetado.ANONIMIZADA,
            modalidad = Modalidad(nombre=entidad.modalidad),
            region= RegionAnatomica (nombre=entidad.region_anatomica),
            patologia= Patologia(nombre=entidad.patologia),
            metadatos= MetadatosImagen(
                resolucion= entidad.resolucion,
                contraste= entidad.contraste,
                tipo = entidad.tipo,
                fase = entidad.fase
            ),
            demografia= Demografia(
                grupo_edad=entidad.grupo_edad,
                sexo=entidad.sexo,
                etnicidad=entidad.etnicidad)
        )
        return imagen_dto

    def dto_a_entidad(self, dto: ImagenDTO) -> Imagen:
        imagen = Imagen()
        imagen.id_proveedor = dto.id_proveedor
        imagen.id_paciente = dto.id_paciente
        imagen.url_path = dto.url_path
        imagen.estado = dto.estado
        imagen.modalidad = Modalidad(nombre=dto.modalidad),
        imagen.region = RegionAnatomica(nombre=dto.region_anatomica),
        imagen.patologia = Patologia(nombre=dto.patologia),
        imagen.metadatos = MetadatosImagen(
            resolucion=dto.resolucion,
            contraste=dto.contraste,
            tipo=dto.tipo,
            fase=dto.fase
        ),
        imagen.demografia = Demografia(
            grupo_edad=dto.grupo_edad,
            sexo=dto.sexo,
            etnicidad=dto.etnicidad)

        return imagen