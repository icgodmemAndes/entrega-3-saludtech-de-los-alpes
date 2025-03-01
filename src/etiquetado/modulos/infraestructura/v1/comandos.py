from pulsar.schema import *
from dataclasses import dataclass, field
from etiquetado.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)
from etiquetado.seedwork.infraestructura.utils import time_millis
from etiquetado.modulos.infraestructura.v1 import TipoCliente
import uuid


class EnriquecerImagen(Record):
    id_proveedor = String(),
    id_paciente = String(),
    url_path = String(),
    estado = String(),
    modalidad = String(),
    region_anatomica = String(),
    patologia = String(),
    resolucion = String(),
    contraste = String(),
    tipo = String(),
    fase = String(),
    grupo_edad = String(),
    sexo = String(),
    etnicidad = String()

class DistribuirDatos(Record):
    id_proveedor: String()
    id_paciente:String()
    url_path: String()
    estado: String()
    etiquetas: Array(String())
    modelo_utilizado: String()
    confianza: Float()

class TagearImagen(Record):
    id_proveedor = String(),
    id_paciente = String(),
    url_path = String(),
    estado = String(),
    modalidad = String(),
    region_anatomica = String(),
    patologia = String(),
    resolucion = String(),
    contraste = String(),
    tipo = String(),
    fase = String(),
    grupo_edad = String(),
    sexo = String(),
    etnicidad = String()

class ComandoEnriquecer(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="Enriquecer")
    datacontenttype = String()
    service_name = String(default="etiquetado.sta")
    data = EnriquecerImagen

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ComandoDistribuirDatos(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="DistribuirDatos")
    datacontenttype = String()
    service_name = String(default="almacenamiento.sta")
    data = DistribuirDatos

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ComandoTagearImagen(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String(default="v1")
    type = String(default="TagearImagen")
    datacontenttype = String()
    service_name = String(default="entrenamiento.sta")
    data = TagearImagen

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)