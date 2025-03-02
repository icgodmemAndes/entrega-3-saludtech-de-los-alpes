from dataclasses import dataclass

from .base import EtiquetadoQueryBaseHandler
from etiquetado.seedwork.aplicacion.queries import ejecutar_query as query
from etiquetado.seedwork.aplicacion.queries import Query, QueryResultado
from etiquetado.modulos.etiquetado.infraestructura.repositorios import RepositorioEtiquetado
from etiquetado.modulos.etiquetado.aplicacion.mapeadores import MapeadorEtiquetado


@dataclass
class ObtenerTodasEtiquetados(Query):
    ...

class ObtenerTodasEtiquetadosHandler(EtiquetadoQueryBaseHandler):

    def handle(self, query: ObtenerTodasEtiquetados) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioEtiquetado.__class__)
        etiquetados = self.fabrica_etiquetado.crear_objeto(repositorio.obtener_todos(), MapeadorEtiquetado())

        return QueryResultado(resultado=etiquetados)

@query.register(ObtenerTodasEtiquetados)
def ejecutar_query_obtener_todas_etiquetados(query: ObtenerTodasEtiquetados):
    handler = ObtenerTodasEtiquetadosHandler()
    return handler.handle(query)