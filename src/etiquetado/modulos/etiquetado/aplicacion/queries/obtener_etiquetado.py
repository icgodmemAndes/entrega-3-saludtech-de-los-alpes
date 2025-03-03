from dataclasses import dataclass

from .base import EtiquetadoQueryBaseHandler
from etiquetado.seedwork.aplicacion.queries import ejecutar_query as query
from etiquetado.seedwork.aplicacion.queries import Query, QueryResultado
from etiquetado.modulos.etiquetado.infraestructura.repositorios import RepositorioEtiquetado
from etiquetado.modulos.etiquetado.aplicacion.mapeadores import MapeadorEtiquetado


@dataclass
class ObtenerEtiquetado(Query):
    id: str


class ObtenerEtiquetadoHandler(EtiquetadoQueryBaseHandler):

    def handle(self, query: ObtenerEtiquetado) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioEtiquetado.__class__)
        etiquetado = self.fabrica_etiquetado.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorEtiquetado())

        return QueryResultado(resultado=etiquetado)


@query.register(ObtenerEtiquetado)
def ejecutar_query_obtener_etiquetado(query: ObtenerEtiquetado):
    handler = ObtenerEtiquetadoHandler()
    return handler.handle(query)
