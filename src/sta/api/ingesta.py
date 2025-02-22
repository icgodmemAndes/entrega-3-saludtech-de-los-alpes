import json
import sta.seedwork.presentacion.api as api
from sta.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request
from flask import Response
from sta.modulos.ingesta.aplicacion.mapeadores import MapeadorIngestaDTOJson
from sta.modulos.ingesta.aplicacion.comandos.crear_ingesta import CrearIngesta
from sta.modulos.ingesta.aplicacion.queries.obtener_ingesta import ObtenerIngesta

from sta.seedwork.aplicacion.comandos import ejecutar_commando
from sta.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('ingesta', '/ingesta')


@bp.route('/crear-ingesta-comando', methods=('POST',))
def crear_ingesta_asincrona():
    try:
        ingesta_dict = request.json

        map_ingesta = MapeadorIngestaDTOJson()
        ingesta_dto = map_ingesta.externo_a_dto(ingesta_dict)

        comando = CrearIngesta(ingesta_dto.id_proveedor, ingesta_dto.id_paciente, ingesta_dto.url_path)

        ejecutar_commando(comando)

        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')


@bp.route('/consulta-por-id/<id>', methods=('GET',))
def dar_reserva_usando_query(id=None):
    if id:
        query_resultado = ejecutar_query(ObtenerIngesta(id))
        map_reserva = MapeadorIngestaDTOJson()

        return map_reserva.dto_a_externo(query_resultado.resultado)
    else:
        return [{'message': 'GET!'}]
