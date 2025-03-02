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
            id_proveedor=str(entidad.id_proveedor),
            id_paciente=str(entidad.id_paciente),
            url_path=entidad.url_path,
            estado=entidad.estado.value,
            fecha_creacion=entidad.fecha_creacion,
        )
        return etiquetado_dto

    def dto_a_entidad(self, dto: EtiquetadoDTO) -> Etiquetado:
        etiquetado = Etiquetado(dto.id, dto.fecha_creacion)
        etiquetado.id_proveedor = dto.id_proveedor
        etiquetado.id_paciente = dto.id_paciente
        etiquetado.url_path = dto.url_path
        etiquetado.estado = dto.estado

        return etiquetado