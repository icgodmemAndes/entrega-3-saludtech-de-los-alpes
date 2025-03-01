import strawberry

from .esquemas import *

@strawberry.type
class Query:
    ingestas: typing.List[Ingesta] = strawberry.field(resolver=obtener_ingestas)