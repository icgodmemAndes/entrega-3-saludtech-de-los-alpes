import strawberry
from strawberry.fastapi import GraphQLRouter

from .consultas import Query
from .mutaciones import Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)
router = GraphQLRouter(schema)