from dataclasses import dataclass

from .base import IngestaQueryBaseHandler
from sta.seedwork.aplicacion.queries import ejecutar_query as query
from sta.seedwork.aplicacion.queries import Query, QueryResultado
from sta.modulos.ingesta.infraestructura.repositorios import RepositorioIngesta
from sta.modulos.ingesta.aplicacion.mapeadores import MapeadorIngesta


@dataclass
class ObtenerIngesta(Query):
    id: str


class ObtenerIngestaHandler(IngestaQueryBaseHandler):

    def handle(self, query: ObtenerIngesta) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioIngesta.__class__)
        ingesta = self.fabrica_ingesta.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorIngesta())

        return QueryResultado(resultado=ingesta)


@query.register(ObtenerIngesta)
def ejecutar_query_obtener_ingesta(query: ObtenerIngesta):
    handler = ObtenerIngestaHandler()
    return handler.handle(query)
