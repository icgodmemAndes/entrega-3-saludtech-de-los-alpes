import uuid

from fastapi import APIRouter, status, BackgroundTasks
from etiquetado.modulos.aplicacion.comandos.distribuir_datos import ComandoDistribuirDatos
from etiquetado.seedwork.presentacion.dto import RespuestaAsincrona
from etiquetado.seedwork.aplicacion.comandos import ejecutar_commando
from etiquetado.seedwork.aplicacion.queries import ejecutar_query

from .dto import DistribuirDatos


router = APIRouter()

@router.post("/distribuir", status_code=status.HTTP_202_ACCEPTED, response_model=RespuestaAsincrona)
async def distrbuir_datos(dato: DistribuirDatos, background_tasks: BackgroundTasks) -> dict[str, str]:
    comando = ComandoDistribuirDatos(
        id_proveedor= uuid.UUID(dato.id_proveedor),
        id_paciente= uuid.UUID(dato.id_paciente),
        url_path= dato.url_path,
        estado= dato.estado,
        etiquetas= dato.etiquetas,
        modelo_utilizado= dato.modelo_utilizado,
        confianza=dato.confianza
        )
    background_tasks.add_task(ejecutar_commando, comando)
    return RespuestaAsincrona(mensaje="Distribucion de datos en proceso")