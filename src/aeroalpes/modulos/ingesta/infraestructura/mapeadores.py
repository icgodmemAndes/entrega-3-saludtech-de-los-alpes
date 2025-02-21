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

        reserva_dto.fecha_creacion = entidad.fecha_creacion
        reserva_dto.fecha_actualizacion = entidad.fecha_actualizacion
        reserva_dto.id = str(entidad.id)

        itinerarios_dto = list()
        
        for itinerario in entidad.itinerarios:
            itinerarios_dto.extend(self._procesar_itinerario(itinerario))

        reserva_dto.itinerarios = itinerarios_dto

        return ingesta_dto

    def dto_a_entidad(self, dto: ReservaDTO) -> Reserva:
        reserva = Reserva(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)
        reserva.itinerarios = list()

        itinerarios_dto: list[ItinerarioDTO] = dto.itinerarios

        reserva.itinerarios.extend(self._procesar_itinerario_dto(itinerarios_dto))
        
        return reserva