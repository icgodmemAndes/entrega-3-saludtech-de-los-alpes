import json
import sta.seedwork.presentacion.api as api
from sta.seedwork.dominio.excepciones import ExcepcionDominio

bp = api.crear_blueprint('imagenes', '/imagenes')
