import asyncio
from typing import Any
from pydantic import BaseSettings
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse

from .api.v1.router import router as v1
from .consumidores import subscribe_to_topic
from .topics import *


class Config(BaseSettings):
    APP_VERSION: str = "2"


settings = Config()
app_configs: dict[str, Any] = {"title": "BFF-Web SaludTech Alpes"}

app = FastAPI(**app_configs)
tasks = list()
events = list()
events_fail = list()
events_admin = list()


def __app_startup_point(topic: str, schema: str, subscription: str, events_recollect: list):
    task = asyncio.ensure_future(
        subscribe_to_topic(
            topic=topic,
            schema=schema,
            subscription=subscription,
            events=events_recollect,
        ),
    )
    tasks.append(task)


@app.on_event("startup")
async def app_startup():
    global tasks
    global events
    global events_fail
    global events_admin

    __app_startup_point(
        topic=event_failed_ingest,
        schema=f"public/default/{event_failed_ingest}",
        subscription='saludtech-bff-fail',
        events_recollect=events_fail,
    )

    __app_startup_point(
        topic=event_ingest_created,
        schema=f"public/default/{event_ingest_created}",
        subscription='saludtech-bff',
        events_recollect=events,
    )
    
    __app_startup_point(
        topic=event_alert_ingest,
        schema=f"public/default/{event_alert_ingest}",
        subscription='saludtech-bff-admin',
        events_recollect=events_admin,
    )


@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()


async def stream_mensajes_from_source(request: Request, event_source: list):
    def print_last_event():
        nonlocal event_source
        event = event_source.pop()
        return {'event': event['topic'], 'data': event['data']}

    async def read_event():
        nonlocal event_source
        while True:
            if await request.is_disconnected():
                break

            if len(event_source) > 0:
                yield print_last_event()

            await asyncio.sleep(0.1)

    return EventSourceResponse(read_event())


@app.get('/bff/stream')
async def stream_mensajes(request: Request):
    global events
    return await stream_mensajes_from_source(request, events)


@app.get('/bff/stream/fails')
async def stream_mensajes(request: Request):
    global events_fail
    return await stream_mensajes_from_source(request, events_fail)


@app.get('/bff/stream/admin')
async def stream_mensajes(request: Request):
    global events_admin
    return await stream_mensajes_from_source(request, events_admin)


@app.get('/bff/version')
async def version():
    return {"version": settings.APP_VERSION}


app.include_router(v1, prefix='/bff/v1')
