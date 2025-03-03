import json
import etiquetado.seedwork.presentacion.api as api
from etiquetado.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request
from flask import Response
from etiquetado.modulos.etiquetado.aplicacion.mapeadores import MapeadorEtiquetadoDTOJson
from etiquetado.modulos.etiquetado.aplicacion.comandos.crear_etiquetado import CrearEtiquetado
from etiquetado.modulos.etiquetado.aplicacion.queries.obtener_etiquetado import ObtenerEtiquetado
from etiquetado.modulos.etiquetado.aplicacion.queries.obtener_todas_etiquetados import ObtenerTodasEtiquetados

from etiquetado.seedwork.aplicacion.comandos import ejecutar_commando
from etiquetado.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('etiquetado', '/etiquetado')


@bp.route('/crear-etiquetado-comando', methods=('POST',))
def crear_etiquetado_asincrona():
    try:
        etiquetado_dict = request.json

        map_etiquetado = MapeadorEtiquetadoDTOJson()
        etiquetado_dto = map_etiquetado.externo_a_dto(etiquetado_dict)

        comando = CrearEtiquetado(etiquetado_dto.id_anonimizado, etiquetado_dto.modalidad, etiquetado_dto.region_anatomica, etiquetado_dto.patologia)

        ejecutar_commando(comando)

        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')


@bp.route('/consulta-por-id/<id>', methods=('GET',))
def dar_reserva_usando_query(id=None):
    if id:
        query_resultado = ejecutar_query(ObtenerEtiquetado(id))
        map_reserva = MapeadorEtiquetadoDTOJson()

        return map_reserva.dto_a_externo(query_resultado.resultado)
    else:
        return [{'message': 'GET!'}]


@bp.route('/todas', methods=('GET',))
def obtener_todas_etiquetados():
    query_resultado = ejecutar_query(ObtenerTodasEtiquetados())
    map_reserva = MapeadorEtiquetadoDTOJson()

    return [map_reserva.dto_a_externo(etiquetado) for etiquetado in query_resultado.resultado]