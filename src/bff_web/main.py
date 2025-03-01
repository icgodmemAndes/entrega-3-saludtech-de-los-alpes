from fastapi import FastAPI, Request
import asyncio

from pydantic import BaseSettings
from typing import Any
from sse_starlette.sse import EventSourceResponse

from .consumidores import suscribirse_a_topico
from .api.v1.router import router as v1
from .despachadores import Despachador


class Config(BaseSettings):
    APP_VERSION: str = "1"


settings = Config()
app_configs: dict[str, Any] = {"title": "BFF-Web SaludTech Alpes"}

app = FastAPI(**app_configs)
tasks = list()
eventos = list()


@app.on_event("startup")
async def app_startup():
    global tasks
    global eventos
    task1 = asyncio.ensure_future(suscribirse_a_topico(
        "eventos-ingesta",
        "saludtech-bff",
        "public/default/eventos-ingesta",
        eventos=eventos,
    ))
    tasks.append(task1)


@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()


@app.get('/stream')
async def stream_mensajes(request: Request):
    def nuevo_evento():
        global eventos
        return {'data': eventos.pop(), 'event': 'NuevoEvento'}

    async def leer_eventos():
        global eventos
        while True:
            if await request.is_disconnected():
                break

            if len(eventos) > 0:
                yield nuevo_evento()

            await asyncio.sleep(0.1)

    return EventSourceResponse(leer_eventos())


app.include_router(v1, prefix='/bff/v1')
