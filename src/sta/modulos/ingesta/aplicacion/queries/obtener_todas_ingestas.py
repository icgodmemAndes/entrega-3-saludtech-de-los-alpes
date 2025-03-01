from dataclasses import dataclass

from .base import IngestaQueryBaseHandler
from sta.seedwork.aplicacion.queries import ejecutar_query as query
from sta.seedwork.aplicacion.queries import Query, QueryResultado
from sta.modulos.ingesta.infraestructura.repositorios import RepositorioIngesta
from sta.modulos.ingesta.aplicacion.mapeadores import MapeadorIngesta


@dataclass
class ObtenerTodasIngestas(Query):
    ...

class ObtenerTodasIngestasHandler(IngestaQueryBaseHandler):

    def handle(self, query: ObtenerTodasIngestas) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioIngesta.__class__)
        ingestas = self.fabrica_ingesta.crear_objeto(repositorio.obtener_todos(), MapeadorIngesta())

        return QueryResultado(resultado=ingestas)

@query.register(ObtenerTodasIngestas)
def ejecutar_query_obtener_todas_ingestas(query: ObtenerTodasIngestas):
    handler = ObtenerTodasIngestasHandler()
    return handler.handle(query)