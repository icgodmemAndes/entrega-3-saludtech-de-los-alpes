import strawberry

from .esquemas import *

@strawberry.type
class Query:
    ingests: typing.List[Ingesta] = strawberry.field(resolver=get_ingests)