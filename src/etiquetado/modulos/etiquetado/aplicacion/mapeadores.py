from .dto import EtiquetadoDTO
from etiquetado.seedwork.aplicacion.dto import Mapeador as AppMap
from etiquetado.seedwork.dominio.repositorios import Mapeador as RepMap
from etiquetado.modulos.etiquetado.dominio.entidades import Etiquetado


class MapeadorEtiquetadoDTOJson(AppMap):

    def externo_a_dto(self, externo: dict) -> EtiquetadoDTO:
        etiquetado_dto = EtiquetadoDTO(
            externo.get('id_proveedor'),
            externo.get('id_paciente'),
            externo.get('url_path'),
            externo.get('estado'),
        )

        return etiquetado_dto

    def dto_a_externo(self, dto: EtiquetadoDTO) -> dict:
        return dto.__dict__


class MapeadorEtiquetado(RepMap):

    def obtener_tipo(self) -> type:
        return Etiquetado.__class__

    def entidad_a_dto(self, entidad: Etiquetado) -> EtiquetadoDTO:
        _id_proveedor = str(entidad.id_proveedor)
        _id_paciente = str(entidad.id_paciente)
        _url_path = str(entidad.url_path)
        _estado = str(entidad.estado)
        _fecha_creacion = str(entidad.fecha_creacion)

        return EtiquetadoDTO(_id_proveedor, _id_paciente, _url_path, _estado, _fecha_creacion)

    def dto_a_entidad(self, dto: EtiquetadoDTO) -> Etiquetado:
        etiquetado = Etiquetado()
        etiquetado.id_proveedor = dto.id_proveedor
        etiquetado.id_paciente = dto.id_paciente
        etiquetado.url_path = dto.url_path
        etiquetado.estado = dto.estado

        return etiquetado
