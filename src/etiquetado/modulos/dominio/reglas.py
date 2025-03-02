"""Reglas de negocio del dominio de cliente

En este archivo usted encontrará reglas de negocio del dominio de cliente

"""

from sta.seedwork.dominio.reglas import ReglaNegocio


class URLValida(ReglaNegocio):

    url: str

    def __init__(self, url, mensaje='La ruta de la imagen debe ser valida'):
        super().__init__(mensaje)
        self.url = url

    def es_valido(self) -> bool:
        return self.url is not None and self.url.startswith('http')