from .dto import IngestaDTO
from sta.seedwork.aplicacion.dto import Mapeador as AppMap
from sta.seedwork.dominio.repositorios import Mapeador as RepMap
from sta.modulos.ingesta.dominio.entidades import Ingesta
from sta.modulos.ingesta.dominio.objetos_valor import EstadoIngesta


class MapeadorIngestaDTOJson(AppMap):

    def externo_a_dto(self, externo: dict) -> IngestaDTO:
        ingesta_dto = IngestaDTO(
            externo.get('id_proveedor'),
            externo.get('id_paciente'),
            externo.get('url_path'),
            EstadoIngesta.PENDIENTE,
        )

        return ingesta_dto

    def dto_a_externo(self, dto: IngestaDTO) -> dict:
        return dto.__dict__


class MapeadorIngesta(RepMap):

    def obtener_tipo(self) -> type:
        return Ingesta.__class__

    def entidad_a_dto(self, entidad: Ingesta) -> IngestaDTO:
        _id_proveedor = str(entidad.id_proveedor)
        _id_paciente = str(entidad.id_paciente)
        _url_path = str(entidad.url_path)
        _estado = str(entidad.estado)

        return IngestaDTO(_id_proveedor, _id_paciente, _url_path, _estado)

    def dto_a_entidad(self, dto: IngestaDTO) -> Ingesta:
        ingesta = Ingesta()
        ingesta.id_proveedor = dto.id_proveedor
        ingesta.id_paciente = dto.id_paciente
        ingesta.url_path = dto.url_path
        ingesta.estado = dto.estado

        return ingesta
