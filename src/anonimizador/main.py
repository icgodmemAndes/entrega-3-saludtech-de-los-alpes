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


app = FastAPI(**app_configs)
tasks: List[asyncio.Task] = []
despachador = Despachador()

# Definir los tópicos y suscripciones a los que se va a conectar el servicio
TOPIC_SUBSCRIPTIONS = [
    ("eventos-ingesta", "sta-sub-eventos", IngestaCreada),
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

def publish_message(payload: Any, message_class: Type, topic: str) -> Dict[str, str]:
    """Helper function to publish messages with common patterns"""
    message = message_class(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=payload.__class__.__name__,
        **{message_class.get_payload_field(): payload}
    )
    despachador.publicar_mensaje(message, topic)
    return {"status": "ok"}

@app.get("/prueba-imagen-anonimizada", include_in_schema=False)
async def prueba_imagen_anonimizada() -> Dict[str, str]:
    payload = ImagenAnonimizada(
        id="1",
        id_ingesta="5beb6c06-3174-4cff-af35-51d337b607d2",
        url_path="aHR0cHM6Ly91cmwuY29t"
    )
    return publish_message(payload, EventoAnonimizacion, "evento-anonimizacion")

@app.get("/limpiar-imagen-raw", include_in_schema=False)
async def limpiar_imagen_raw() -> Dict[str, str]:
    payload = LimpiarIngesta(id_ingesta="5beb6c06-3174-4cff-af35-51d337b607d2")
    return publish_message(payload, ComandoLimpiarIngesta, "comando-eliminar-ingesta")

@app.get("/health", include_in_schema=False)
async def health() -> Dict[str, str]:
    return {"status": "ok"}

# Include router at the end
app.include_router(v1, prefix="/v1", tags=["Version 1"])
