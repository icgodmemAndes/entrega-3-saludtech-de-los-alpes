import os
import typing
import strawberry
import requests
from datetime import datetime

SALUDTECH_ALPES_HOST = os.getenv("SALUDTECH_ALPES_ADDRESS", default="localhost")
FORMATO_FECHA = '%Y-%m-%d %H:%M:%S'


def obtener_ingestas(root) -> typing.List["Ingesta"]:
    ingestas_json = requests.get(f'http://{SALUDTECH_ALPES_HOST}:5000/ingesta/todas').json()
    ingestas = []

    for ingesta in ingestas_json:
        ingestas.append(
            Ingesta(
                id_proveedor=ingesta.get('id_proveedor'),
                id_paciente=ingesta.get('id_paciente'),
                url_path=ingesta.get('url_path'),
                estado=ingesta.get('estado'),
                fecha_creacion=datetime.strptime(ingesta.get('fecha_creacion'), FORMATO_FECHA)
            )
        )

    return ingestas


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
