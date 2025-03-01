from etiquetado.seedwork.aplicacion.queries import Query, QueryHandler, ResultadoQuery
import uuid

class ObtenerTodosImagenes(Query):
    ...

class ObtenerTodosUsuariosHandler(QueryHandler):

    def handle() -> ResultadoQuery:
        ...