import os
import typing
import strawberry
import requests
from datetime import datetime

FORMATO_FECHA = '%Y-%m-%d %H:%M:%S'
SALUDTECH_ALPES_HOST = os.getenv("SALUDTECH_ALPES_ADDRESS", default="localhost")


def get_ingests(root) -> typing.List["Ingesta"]:
    ingests_json = requests.get(f'http://{SALUDTECH_ALPES_HOST}:5000/ingesta/todas').json()
    ingests = []

    for ingest in ingests_json:
        ingests.append(
            Ingesta(
                id_proveedor=ingest.get('id_proveedor'),
                id_paciente=ingest.get('id_paciente'),
                url_path=ingest.get('url_path'),
                estado=ingest.get('estado'),
                fecha_creacion=datetime.strptime(ingest.get('fecha_creacion'), FORMATO_FECHA)
            )
        )

    return ingests


@strawberry.type
class Ingesta:
    id_proveedor: str
    id_paciente: str
    url_path: str
    estado: str
    fecha_creacion: datetime


@strawberry.type
class IngestaRespuesta:
    mensaje: str
    codigo: int
