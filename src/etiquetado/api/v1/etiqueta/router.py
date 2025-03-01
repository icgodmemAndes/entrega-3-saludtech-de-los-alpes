import uuid

from fastapi import APIRouter, status, BackgroundTasks
from etiquetado.modulos.aplicacion.comandos.tagear_imagen import ComandoTagearImagen
from etiquetado.seedwork.presentacion.dto import RespuestaAsincrona
from etiquetado.seedwork.aplicacion.comandos import ejecutar_commando
from etiquetado.seedwork.aplicacion.queries import ejecutar_query

from .dto import TagearImagen


router = APIRouter()

@router.post("/tagear", status_code=status.HTTP_202_ACCEPTED, response_model=RespuestaAsincrona)
async def tagear_imagen(tagear_imagen: TagearImagen, background_tasks: BackgroundTasks) -> dict[str, str]:
    comando = ComandoTagearImagen(
        id_proveedor= uuid.UUID(tagear_imagen.id_proveedor),
        id_paciente= uuid.UUID(tagear_imagen.id_paciente),
        url_path= tagear_imagen.url_path,
        estado= tagear_imagen.estado,
        modalidad= tagear_imagen.modalidad,
        region_anatomica= tagear_imagen.region_anatomica,
        patologia= tagear_imagen.patologia,
        resolucion= tagear_imagen.resolucion,
        contraste= tagear_imagen.contraste,
        tipo= tagear_imagen.tipo,
        fase= tagear_imagen.fase,
        grupo_edad= tagear_imagen.grupo_edad,
        sexo= tagear_imagen.sexo,
        etnicidad= tagear_imagen.etnicidad
        )
    background_tasks.add_task(ejecutar_commando, comando)
    return RespuestaAsincrona(mensaje="Tageo de imagen en proceso")