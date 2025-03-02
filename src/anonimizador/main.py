from fastapi import FastAPI
from typing import List, Dict
import asyncio
from datetime import datetime

from anonimizador.config.api import app_configs
from anonimizador.api.v1.router import router as v1

# These are your background tasks (the consumers listening to Pulsar topics)
from anonimizador.modulos.infraestructura.consumidores import suscribirse_a_topico

# Imports for your schema-based messages
from anonimizador.modulos.infraestructura.v1.eventos import IngestaCreada, ImagenAnonimizada
from anonimizador.modulos.infraestructura.v1.comandos import ComandoLimpiarIngesta, LimpiarIngesta, IngestaCreadaPayload

# The "despachador" object that publishes messages
from anonimizador.modulos.infraestructura.despachadores import Despachador
from anonimizador.seedwork.infraestructura import utils

from sqlalchemy import text
from anonimizador.config.db import Base, engine




app = FastAPI(**app_configs)
tasks: List[asyncio.Task] = []
despachador = Despachador()

# Define the topic-subscription pairs
TOPIC_SUBSCRIPTIONS = [
    ("eventos-ingesta", "sta-ingesta", IngestaCreada)
]

@app.on_event("startup")
async def app_startup():

    print("[DB-Init] Running...")

    custom_schema = 'massive_worker'
    with engine.connect() as connection:
        connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {custom_schema}"))
        Base.metadata.schema = custom_schema
        Base.metadata.create_all(engine)
    print("[DB-Init] Finished")

    """
    On startup, schedule background tasks that listen to the specified topics.
    """
    for topic, subscription, message_type in TOPIC_SUBSCRIPTIONS:
        tasks.append(asyncio.ensure_future(
            suscribirse_a_topico(topic, subscription, message_type)
        ))

@app.on_event("shutdown")
def shutdown_event():
    """
    On shutdown, cancel all background tasks (Pulsar consumers).
    """
    for task in tasks:
        task.cancel()

@app.get("/ingesta-creada", include_in_schema=False)
async def prueba_ingesta_creada() -> Dict[str, str]:
    """
    Endpoint that publishes a test 'IngestaCreada' message to the 'eventos-ingesta' topic.
    We return a simple JSON dict to avoid returning any non-serializable objects.
    """
    payload = IngestaCreadaPayload(
        id_ingesta="5beb6c06-3174-4cff-af35-51d337b607d2",
        id_proveedor="1",
        id_paciente="1",
        url_path="aHR0cHM6Ly91cmwuY29t",
        estado="creada",
        fecha_creacion=str(datetime.now())
    )
    print("Se va publicar mensaje de prueba IngestaCreada...")
    # Publish the message, but don't return the raw publisher result
    despachador.publicar_mensaje(payload, "eventos-ingesta")
    # Return a simple dict or message
    return {"status": "published", "payload": payload.id_ingesta}

@app.get("/prueba-imagen-anonimizada", include_in_schema=False)
async def prueba_imagen_anonimizada() -> Dict[str, str]:
    """
    Endpoint that publishes a test 'ImagenAnonimizada' message to the 'eventos-ingesta' topic.
    """
    payload = ImagenAnonimizada(
        id="1",
        id_ingesta="5beb6c06-3174-4cff-af35-51d337b607d2",
        url_path="aHR0cHM6Ly91cmwuY29t"
    )
    despachador.publicar_mensaje(payload, "eventos-ingesta")
    return {"status": "published", "payload": payload.id_ingesta}

@app.get("/limpiar-imagen-raw", include_in_schema=False)
async def limpiar_imagen_raw() -> Dict[str, str]:
    """
    Endpoint that publishes a 'LimpiarIngesta' command to the 'eventos-ingesta' topic.
    """
    payload = LimpiarIngesta(id_ingesta="5beb6c06-3174-4cff-af35-51d337b607d2")
    despachador.publicar_mensaje(payload, "eventos-ingesta")
    return {"status": "published", "payload": payload.id_ingesta}

@app.get("/health", include_in_schema=False)
async def health() -> Dict[str, str]:
    """
    Simple healthcheck endpoint.
    """
    return {"status": "ok"}

# Include your other API router at the end
app.include_router(v1, prefix="/v1", tags=["Version 1"])