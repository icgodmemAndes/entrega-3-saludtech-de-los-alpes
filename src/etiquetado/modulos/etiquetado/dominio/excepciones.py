""" Excepciones del dominio de vuelos

En este archivo usted encontrará los Excepciones relacionadas
al dominio de vuelos

"""

from etiquetado.seedwork.dominio.excepciones import ExcepcionFabrica

class TipoObjetoNoExisteEnDominioEtiquetadoExcepcion(ExcepcionFabrica):
    def __init__(self, mensaje='No existe una fábrica para el tipo solicitado en el módulo de etiquetado'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)

class TipoObjetoNoExisteEnDominioTagearExcepcion(ExcepcionFabrica):
    def __init__(self, mensaje='No existe una fábrica para el tipo solicitado en el módulo de tagear'):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)