from fastapi import FastAPI
from typing import List, Dict, Any, Type, Callable
import asyncio

from anonimizador.config.api import app_configs
from anonimizador.api.v1.router import router as v1
from anonimizador.modulos.infraestructura.consumidores import suscribirse_a_topico
from anonimizador.modulos.infraestructura.v1.eventos import EventoAnonimizacion, IngestaCreada, ImagenAnonimizada
from anonimizador.modulos.infraestructura.v1.comandos import ComandoLimpiarIngesta, LimpiarIngesta
from anonimizador.modulos.infraestructura.despachadores import Despachador
from anonimizador.seedwork.infraestructura import utils
from anonimizador.modulos.infraestructura.v1.comandos import IngestaCreadaPayload

from datetime import datetime

app = FastAPI(**app_configs)
tasks: List[asyncio.Task] = []
despachador = Despachador()

# Definir los tópicos y suscripciones a los que se va a conectar el servicio
TOPIC_SUBSCRIPTIONS = [
    ("eventos-ingesta", "sta-ingesta", IngestaCreada)
]

@app.on_event("startup")
async def app_startup():
    for topic, subscription, message_type in TOPIC_SUBSCRIPTIONS:
        tasks.append(asyncio.ensure_future(
            suscribirse_a_topico(topic, subscription, message_type)
        ))

@app.on_event("shutdown")
def shutdown_event():
    for task in tasks:
        task.cancel()


@app.get("/ingesta-creada", include_in_schema=False)
async def prueba_ingesta_creada() -> Dict[str, str]:
    payload = IngestaCreadaPayload(        
        id_ingesta="5beb6c06-3174-4cff-af35-51d337b607d2",
        id_proveedor = "1",
        id_paciente = "1",
        url_path="aHR0cHM6Ly91cmwuY29t",
        estado="creada",
        fecha_creacion = str(datetime.now())
    )

    print(f'Se va publicar mensaje de prueba IngestaCreada...')
    return despachador.publicar_mensaje(payload, "eventos-ingesta")


@app.get("/prueba-imagen-anonimizada", include_in_schema=False)
async def prueba_imagen_anonimizada() -> Dict[str, str]:
    payload = ImagenAnonimizada(
        id="1",
        id_ingesta="5beb6c06-3174-4cff-af35-51d337b607d2",
        url_path="aHR0cHM6Ly91cmwuY29t"
    )
    return despachador.publicar_mensaje(payload, "eventos-ingesta")

@app.get("/limpiar-imagen-raw", include_in_schema=False)
async def limpiar_imagen_raw() -> Dict[str, str]:
    payload = LimpiarIngesta(id_ingesta="5beb6c06-3174-4cff-af35-51d337b607d2")
    return despachador.publicar_mensaje(payload, "eventos-ingesta")

@app.get("/health", include_in_schema=False)
async def health() -> Dict[str, str]:
    return {"status": "ok"}

# Include router at the end
app.include_router(v1, prefix="/v1", tags=["Version 1"])
