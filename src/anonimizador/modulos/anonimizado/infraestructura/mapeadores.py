import base64
from anonimizador.seedwork.dominio.repositorios import Mapeador
from anonimizador.modulos.anonimizado.dominio.entidades import Anonimizado
from .dto import Anonimizado as AnonimizadoDTO


def convertir_a_base64(cadena: str) -> str:
    bytes_cadena = cadena.encode('utf-8')
    base64_bytes = base64.b64encode(bytes_cadena)
    base64_cadena = base64_bytes.decode('utf-8')
    return base64_cadena[:1000]

def revertir_base64(cadena: str) -> str:
    base64_bytes = cadena.encode('utf-8')
    bytes_cadena = base64.b64decode(base64_bytes)
    cadena = bytes_cadena.decode('utf-8')
    return cadena


class MapeadorAnonimizado(Mapeador):

    def obtener_tipo(self) -> type:
        return Anonimizado.__class__

    def entidad_a_dto(self, entidad: Anonimizado) -> AnonimizadoDTO:
        anonimizado_dto = AnonimizadoDTO(
            id=str(entidad.id),
            id_ingesta=str(entidad.id_ingesta),
            url_path=convertir_a_base64(entidad.url_path),
        )
        return anonimizado_dto

    def dto_a_entidad(self, dto: AnonimizadoDTO) -> Anonimizado:
        anonimizado = Anonimizado()
        anonimizado.id_ingesta = dto.id_ingesta
        anonimizado.url_path = dto.url_path

        return anonimizado
    
class MapeadorRevertirAnonimizado(Mapeador):

    def obtener_tipo(self) -> type:
        return Anonimizado.__class__

    def entidad_a_dto(self, entidad: Anonimizado) -> AnonimizadoDTO:
        anonimizado_dto = AnonimizadoDTO(                
            id=str(entidad.id_anonimizado),
        )
        return anonimizado_dto

    def dto_a_entidad(self, dto: AnonimizadoDTO) -> Anonimizado:
        anonimizado = Anonimizado(dto.id_anonimizado)
        anonimizado._id = dto.id_anonimizado

        return anonimizado
