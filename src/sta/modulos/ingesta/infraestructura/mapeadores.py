""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from sta.seedwork.dominio.repositorios import Mapeador
from sta.modulos.ingesta.dominio.objetos_valor import EstadoIngesta
from sta.modulos.ingesta.dominio.entidades import Ingesta
from .dto import Ingesta as IngestaDTO

class MapeadorIngesta(Mapeador):

    def obtener_tipo(self) -> type:
        return Ingesta.__class__

    def entidad_a_dto(self, entidad: Ingesta) -> IngestaDTO:
        ingesta_dto = IngestaDTO(            
            id_proveedor=str(entidad.id_proveedor),
            id_paciente=str(entidad.id_paciente),
            url_path=entidad.url_path,
            estado=entidad.estado.value,
            id=str(entidad.id)
        )
        return ingesta_dto

    def dto_a_entidad(self, dto: IngestaDTO) -> Ingesta:
        ingesta = Ingesta(dto.id_proveedor, dto.id_paciente, dto.url_path, dto.estado)

        return ingesta