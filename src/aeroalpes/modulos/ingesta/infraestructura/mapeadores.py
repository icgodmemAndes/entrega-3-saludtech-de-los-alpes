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
        ingesta_dto.id = str(entidad.id)

        return ingesta_dto

    def dto_a_entidad(self, dto: IngestaDTO) -> Ingesta:
        reserva = Ingesta(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)
        reserva.itinerarios = list()

        return reserva