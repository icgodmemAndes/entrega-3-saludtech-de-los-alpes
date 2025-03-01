import typing
import uuid
import strawberry

from strawberry.types import Info
from bff_web import utils
from bff_web.despachadores import Despachador

from .esquemas import *


@strawberry.type
class Mutation:

    @strawberry.mutation
    async def crear_ingesta(self, id_proveedor: str, id_paciente: str, url_path: str, info: Info) -> IngestaRespuesta:
        print(f"ID Proveedor: {id_proveedor}, ID Paciente: {id_paciente}, URL Path: {url_path}")
        payload = dict(
            id_proveedor=id_proveedor,
            id_paciente=id_paciente,
            url_path=url_path
        )
        comando = dict(
            id=str(uuid.uuid4()),
            time=utils.time_millis(),
            specversion="v1",
            type="ComandoIngesta",
            ingestion=utils.time_millis(),
            datacontenttype="AVRO",
            service_name="BFF Web",
            data=payload
        )
        despachador = Despachador()
        info.context["background_tasks"].add_task(despachador.publicar_mensaje, comando, "comando-crear-ingesta",
                                                  "public/default/comando-crear-ingesta")

        return IngestaRespuesta(mensaje="Procesando Mensaje", codigo=203)
