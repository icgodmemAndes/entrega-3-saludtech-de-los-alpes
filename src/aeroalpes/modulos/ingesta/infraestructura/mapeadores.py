""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from aeroalpes.seedwork.dominio.repositorios import Mapeador
from aeroalpes.modulos.ingesta.dominio.objetos_valor import EstadoIngesta
from aeroalpes.modulos.ingesta.dominio.entidades import Ingesta
from .dto import Ingesta as IngestaDTO

class MapeadorIngesta(Mapeador):

    def obtener_tipo(self) -> type:
        return Ingesta.__class__

    def entidad_a_dto(self, entidad: Ingesta) -> IngestaDTO:
        
        ingesta_dto = IngestaDTO()
        ingesta_dto.id_proveedor = str(entidad.id_proveedor)
        ingesta_dto.id_paciente = str(entidad.id_paciente)
        ingesta_dto.url_path = str(entidad.url_path)
        ingesta_dto.estado = str(entidad.estado)

        return ingesta_dto

    def dto_a_entidad(self, dto: IngestaDTO) -> Ingesta:
        ingesta = Ingesta(dto.id_proveedor, dto.id_paciente, dto.url_path, dto.estado)

        return ingesta