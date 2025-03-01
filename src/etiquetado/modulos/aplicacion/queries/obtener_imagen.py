from etiquetado.seedwork.aplicacion.queries import Query, QueryHandler, ResultadoQuery
import uuid

class ObtenerImagen(Query):
    imagen_id: uuid.UUID

class ObtenerUsuarioHandler(QueryHandler):

    def handle() -> ResultadoQuery:
        ...