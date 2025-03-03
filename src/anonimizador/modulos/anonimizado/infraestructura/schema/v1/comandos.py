from pulsar.schema import *
from anonimizador.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion


class IniciarEtiquetadoPayload(Record):
    id_anonimizado = String()
    modalidad = String()
    region_anatomica = String()
    patologia = String()


class IniciarEtiquetado(ComandoIntegracion):
    data = IniciarEtiquetadoPayload()


class EliminarIngestaPayload(Record):
    id_ingesta = String()


class EliminarIngesta(ComandoIntegracion):
    data = EliminarIngestaPayload()
