from .dto import EtiquetadoDTO
from etiquetado.seedwork.aplicacion.dto import Mapeador as AppMap
from etiquetado.seedwork.dominio.repositorios import Mapeador as RepMap
from etiquetado.modulos.etiquetado.dominio.entidades import Etiquetado


class MapeadorEtiquetadoDTOJson(AppMap):

    def externo_a_dto(self, externo: dict) -> EtiquetadoDTO:
        etiquetado_dto = EtiquetadoDTO(
            externo.get('id_anonimizado'),
            externo.get('modalidad'),
            externo.get('region_anatomica'),
            externo.get('patologia'),
        )

        return etiquetado_dto

    def dto_a_externo(self, dto: EtiquetadoDTO) -> dict:
        return dto.__dict__


class MapeadorEtiquetado(RepMap):

    def obtener_tipo(self) -> type:
        return Etiquetado.__class__

    def entidad_a_dto(self, entidad: Etiquetado) -> EtiquetadoDTO:
        _id_anonimizado = str(entidad.id_anonimizado)
        _modalidad = str(entidad.modalidad)
        _region_anatomica = str(entidad.region_anatomica)
        _patologia = str(entidad.patologia)
        #_estado = str(entidad.estado)
        _fecha_creacion = str(entidad.fecha_creacion)

        return EtiquetadoDTO(_id_anonimizado, _modalidad, _region_anatomica,_patologia , _fecha_creacion)

    def dto_a_entidad(self, dto: EtiquetadoDTO) -> Etiquetado:
        etiquetado = Etiquetado()
        etiquetado.id_anonimizado = dto.id_anonimizado
        etiquetado.modalidad = dto.modalidad
        etiquetado.region_anatomica = dto.region_anatomica
        etiquetado.patologia = dto.patologia
        #etiquetado.estado = dto.estado

        return etiquetado
