import uuid
import strawberry
from strawberry.types import Info

from bff_web import utils
from bff_web.despachadores import Dispatcher
from bff_web.topics import command_create_ingest

from .esquemas import *


@strawberry.type
class Mutation:

    @strawberry.mutation
    async def create_ingest(self, provider_id: str, patient_id: str, url_path: str, info: Info) -> IngestaRespuesta:
        payload = dict(
            id_proveedor=provider_id,
            id_paciente=patient_id,
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
        dispatcher = Dispatcher()
        info.context["background_tasks"].add_task(
            dispatcher.publish_message,
            comando,
            command_create_ingest,
            f"public/default/{command_create_ingest}",
        )

        return IngestaRespuesta(mensaje="Procesando Mensaje", codigo=203)
