import json
import etiquetado.seedwork.presentacion.api as api
from etiquetado.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request
from flask import Response
from etiquetado.modulos.etiquetado.aplicacion.mapeadores import MapeadorEtiquetadoDTOJson, MapeadorRevertirDTOJson
from etiquetado.modulos.etiquetado.aplicacion.comandos.crear_etiquetado import CrearEtiquetado

from etiquetado.seedwork.aplicacion.comandos import ejecutar_commando

bp = api.crear_blueprint('etiquetado', '/etiquetado')


@bp.route('/crear-etiquetado-comando', methods=('POST',))
def crear_etiquetado_asincrona():
    try:
        etiquetado_dict = request.json

        map_etiquetado = MapeadorEtiquetadoDTOJson()
        etiquetado_dto = map_etiquetado.externo_a_dto(etiquetado_dict)

        comando = CrearEtiquetado(etiquetado_dto.id_anonimizado, etiquetado_dto.modalidad,
                                  etiquetado_dto.region_anatomica, etiquetado_dto.patologia)

        ejecutar_commando(comando)

        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
