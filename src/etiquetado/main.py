from fastapi import FastAPI
from etiquetado.config.api import app_configs, settings
from etiquetado.api.v1.router import router as v1

from etiquetado.modulos.infraestructura.consumidores import suscribirse_a_topico
from etiquetado.modulos.infraestructura.v1.eventos import EventoImagenTageada, ImagenTageada
from etiquetado.modulos.infraestructura.v1.comandos import ComandoEnriquecer, ComandoDistribuirDatos,ComandoTagearImagen,EnriquecerImagen,TagearImagen,DistribuirDatos
from etiquetado.modulos.infraestructura.despachadores import Despachador
from etiquetado.seedwork.infraestructura import utils

import asyncio
import time
import traceback
import uvicorn

from src.etiquetado.modulos.infraestructura.v1 import EstadoEtiquetado

app = FastAPI(**app_configs)
tasks = list()

@app.on_event("startup")
async def app_startup():
    global tasks
    task1 = asyncio.ensure_future(suscribirse_a_topico("evento-imagen-tageada", "sub-imagen-tageada", EventoImagenTageada))
    task2 = asyncio.ensure_future(suscribirse_a_topico("comando-enriquecer", "sub-com-enriquecer", ComandoEnriquecer))
    task3 = asyncio.ensure_future(suscribirse_a_topico("comando-distribuir-datos", "sub-com-distribuir-datos", ComandoDistribuirDatos))
    task4 = asyncio.ensure_future(suscribirse_a_topico("comando-tagear-imagen", "sub-com-tagear-imagen", ComandoTagearImagen))
    tasks.append(task1)
    tasks.append(task2)
    tasks.append(task3)
    tasks.append(task4)

@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()

@app.get("/prueba-imagen-tageada", include_in_schema=False)
async def prueba_imagen_tageada() -> dict[str, str]:
    payload = ImagenTageada(
        id_proveedor = "410ac987-c973-4b83-ab90-44d5dd9dc0b6",
        id_paciente = "5e134baa-a0db-41b9-b769-d91aab1acfbd",
        url_path = "http://XXXXXXXXXXXXXXX",
        estado = EstadoEtiquetado.FINALIZADA,
        etiquetas=["tumor", "tirads 5", "inflammation"],
        modelo_utilizado= "AI-Model-V1",
        confianza = 0.95
    )
    evento = EventoImagenTageada(
        time=utils.time_millis(),
        datacontenttype=ImagenTageada.__name__,
        imagen_tageada = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(evento, "evento-imagen-tageada")
    return {"status": "ok"}

@app.get("/prueba-enriquecer", include_in_schema=False)
async def prueba_enriquecer() -> dict[str, str]:
    payload = EnriquecerImagen(
        id_proveedor = "410ac987-c973-4b83-ab90-44d5dd9dc0b6",
        id_paciente = "5e134baa-a0db-41b9-b769-d91aab1acfbd",
        url_path = "http://XXXXXXXXXXXXXXX",
        estado = EstadoEtiquetado.CREADA,
        modalidad = "Rayos X",
        region_anatomica = "Cerebro",
        patologia = "Tumor",
        resolucion = "1920x1080",
        contraste = "Alto",
        tipo = "2D",
        fase = "Pre-tratamiento",
        grupo_edad = "Adulto",
        sexo = "Masculino",
        etnicidad = "Latino",
    )

    comando = ComandoEnriquecer(
        time=utils.time_millis(),
        datacontenttype=EnriquecerImagen.__name__,
        data=payload
    )

    despachador = Despachador()
    despachador.publicar_mensaje(comando, "comando-enriquecer")
    return {"status": "ok"}


@app.get("/prueba-distribuir-datos", include_in_schema=False)
async def prueba_distribuir_datos() -> dict[str, str]:

    payload = DistribuirDatos(
        id_proveedor="410ac987-c973-4b83-ab90-44d5dd9dc0b6",
        id_paciente="5e134baa-a0db-41b9-b769-d91aab1acfbd",
        url_path="http://XXXXXXXXXXXXXXX",
        estado=EstadoEtiquetado.FINALIZADA,
        etiquetas=["tumor", "tirads 5", "inflammation"],
        modelo_utilizado="AI-Model-V1",
        confianza=0.95
    )

    comando = ComandoDistribuirDatos(
        time=utils.time_millis(),
        datacontenttype=DistribuirDatos.__name__,
        data=payload
    )

    despachador = Despachador()
    despachador.publicar_mensaje(comando, "comando-distribuir-datos")
    return {"status": "ok"}


@app.get("/prueba-tagear-imagen", include_in_schema=False)
async def prueba_tagear_imagen() -> dict[str, str]:
    payload = TagearImagen(
        id_proveedor="410ac987-c973-4b83-ab90-44d5dd9dc0b6",
        id_paciente="5e134baa-a0db-41b9-b769-d91aab1acfbd",
        url_path="http://XXXXXXXXXXXXXXX",
        estado=EstadoEtiquetado.PENDIENTE,
        modalidad="Rayos X",
        region_anatomica="Cerebro",
        patologia="Tumor",
        resolucion="1920x1080",
        contraste="Alto",
        tipo="2D",
        fase="Pre-tratamiento",
        grupo_edad="Adulto",
        sexo="Masculino",
        etnicidad="Latino",
    )

    comando = ComandoTagearImagen(
        time=utils.time_millis(),
        datacontenttype=TagearImagen.__name__,
        data=payload
    )

    despachador = Despachador()
    despachador.publicar_mensaje(comando, "comando-tagear-imagen")
    return {"status": "ok"}

@app.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(v1, prefix="/v1", tags=["Version 1"])
