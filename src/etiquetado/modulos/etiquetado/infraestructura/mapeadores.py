""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from etiquetado.seedwork.dominio.repositorios import Mapeador
from etiquetado.modulos.etiquetado.dominio.entidades import Etiquetado
from .dto import Etiquetado as EtiquetadoDTO

class MapeadorEtiquetado(Mapeador):

    def obtener_tipo(self) -> type:
        return Etiquetado.__class__

    def entidad_a_dto(self, entidad: Etiquetado) -> EtiquetadoDTO:
        etiquetado_dto = EtiquetadoDTO(
            id=str(entidad.id),
            id_anonimizado=str(entidad.id_anonimizado),
            modalidad=str(entidad.modalidad),
            region_anatomica=entidad.region_anatomica,
            patologia=entidad.patologia,
            fecha_creacion=entidad.fecha_creacion,
        )
        return etiquetado_dto

    def dto_a_entidad(self, dto: EtiquetadoDTO) -> Etiquetado:
        etiquetado = Etiquetado(dto.id, dto.fecha_creacion)
        etiquetado.id_anonimizado = dto.id_anonimizado
        etiquetado.modalidad = dto.modalidad
        etiquetado.region_anatomica = dto.region_anatomica
        etiquetado.patologia = dto.patologia

        return etiquetado