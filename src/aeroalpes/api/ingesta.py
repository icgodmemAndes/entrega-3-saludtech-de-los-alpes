import aeroalpes.seedwork.presentacion.api as api
import json
from aeroalpes.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request
from flask import Response
from aeroalpes.modulos.ingesta.aplicacion.mapeadores import MapeadorIngestaDTOJson
from aeroalpes.modulos.ingesta.aplicacion.comandos.crear_ingesta import CrearIngesta

from aeroalpes.seedwork.aplicacion.comandos import ejecutar_commando

bp = api.crear_blueprint('ingesta', '/ingesta')


@bp.route('/crear-ingesta-comando', methods=('POST',))
def crear_ingesta_asincrona():
    try:
        ingesta_dict = request.json

        map_ingesta = MapeadorIngestaDTOJson()
        ingesta_dto = map_ingesta.externo_a_dto(ingesta_dict)

        comando = CrearIngesta(ingesta_dto.id_proveedor, ingesta_dto.id_paciente, ingesta_dto.url_path)
        
        # TODO Reemplaze es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
