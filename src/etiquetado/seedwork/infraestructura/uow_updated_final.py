from abc import ABC, abstractmethod
from enum import Enum

from etiquetado.seedwork.dominio.entidades import AgregacionRaiz
from pydispatch import dispatcher

import pickle
import logging
import traceback
import asyncio


class Lock(Enum):
    OPTIMISTA = 1
    PESIMISTA = 2


class Batch:
    def __init__(self, operacion, lock: Lock, *args, **kwargs):
        self.operacion = operacion
        self.args = args
        self.kwargs = kwargs
        self.lock = lock


class UnidadTrabajo(ABC):

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def _obtener_eventos_rollback(self, batches=None):
        batches = self.batches if batches is None else batches
        eventos = list()
        for batch in batches:
            for arg in batch.args:
                if isinstance(arg, AgregacionRaiz):
                    eventos += arg.eventos_rollback
        return eventos

    def _obtener_eventos(self, batches=None):
        batches = self.batches if batches is None else batches
        eventos = list()
        for batch in batches:
            for arg in batch.args:
                if isinstance(arg, AgregacionRaiz):
                    eventos += arg.eventos
        return eventos

    @abstractmethod
    def _limpiar_batches(self):
        raise NotImplementedError

    @abstractmethod
    def batches(self) -> list[Batch]:
        raise NotImplementedError

    @abstractmethod
    def savepoints(self) -> list:
        raise NotImplementedError
    
    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self, savepoint=None):
        raise NotImplementedError
    
    @abstractmethod
    def savepoint(self):
        raise NotImplementedError

    def registrar_batch(self, operacion, *args, lock=Lock.PESIMISTA, repositorio_eventos_func=None,**kwargs):
        batch = Batch(operacion, lock, *args, **kwargs)
        self.batches.append(batch)
        self._publicar_eventos_dominio(batch, repositorio_eventos_func)

    def _publicar_eventos_dominio(self, batch, repositorio_eventos_func):
        eventos = self._obtener_eventos(batches=[batch])
        for evento in eventos:
            if repositorio_eventos_func:
                repositorio_eventos_func(evento)

    def _publicar_eventos_post_commit(self):
        eventos = self._obtener_eventos()
        for evento in eventos:
            dispatcher.send(signal=f'{type(evento).__name__}Dominio', evento=evento)


def is_flask():
    try:
        from flask import session
        return True
    except Exception as e:
        return False

def is_fastapi():
    try:
        import fastapi
        return True
    except Exception as e:
        return False

def registrar_unidad_de_trabajo(serialized_obj):
    from etiquetado.config.uow import UnidadTrabajoSQLAlchemy
    from flask import session
    
    session['uow'] = serialized_obj

def flask_uow():
    from flask import session
    from etiquetado.config.uow import UnidadTrabajoSQLAlchemy
    if session.get('uow'):
        return session['uow']

    uow_serialized = pickle.dumps(UnidadTrabajoSQLAlchemy())
    registrar_unidad_de_trabajo(uow_serialized)
    return uow_serialized

async def fastapi_uow():
    # Get the request state to store/retrieve UoW
    try:
        from fastapi import Request
        from etiquetado.config.uow import UnidadTrabajoSQLAlchemy
        
        # Note: This requires proper request context setup
        request = Request.get_current()
        
        # Check if UoW is already in the request state
        if hasattr(request.state, 'uow'):
            return request.state.uow
        
        # Create a new UnidadTrabajoSQLAlchemy and store it in request state
        uow = UnidadTrabajoSQLAlchemy()
        request.state.uow = uow
        return uow
    except Exception as e:
        # Fallback if not in request context or other error
        from etiquetado.config.uow import UnidadTrabajoSQLAlchemy
        return UnidadTrabajoSQLAlchemy()

def unidad_de_trabajo() -> UnidadTrabajo:
    if is_flask():
        return pickle.loads(flask_uow())
    else:
        raise Exception('No hay unidad de trabajo')

async def unidad_de_trabajo_async() -> UnidadTrabajo:
    if is_fastapi():
        return await fastapi_uow()
    else:
        raise Exception('No hay unidad de trabajo asíncrona configurada')

def guardar_unidad_trabajo(uow: UnidadTrabajo):
    if is_flask():
        from flask import session
        session['uow'] = pickle.dumps(uow)


class UnidadTrabajoPuerto:
    @staticmethod
    def commit():
        with unidad_de_trabajo() as uow:
            uow.commit()

    @staticmethod
    def rollback(savepoint=None):
        with unidad_de_trabajo() as uow:
            uow.rollback(savepoint=savepoint)

    @staticmethod
    def savepoint():
        with unidad_de_trabajo() as uow:
            return uow.savepoint()

    @staticmethod
    def dar_savepoints():
        with unidad_de_trabajo() as uow:
            return uow.savepoints()

    @staticmethod
    def registrar_batch(operacion, *args, lock=Lock.PESIMISTA, **kwargs):
        with unidad_de_trabajo() as uow:
            return uow.registrar_batch(operacion, *args, lock=lock, **kwargs)

class UnidadTrabajoPuertoAsync:
    @staticmethod
    async def commit():
        uow = await unidad_de_trabajo_async()
        await uow.commit()

    @staticmethod
    async def rollback(savepoint=None):
        uow = await unidad_de_trabajo_async()
        await uow.rollback(savepoint=savepoint)

    @staticmethod
    async def savepoint():
        uow = await unidad_de_trabajo_async()
        return await uow.savepoint()

    @staticmethod
    async def dar_savepoints():
        uow = await unidad_de_trabajo_async()
        return uow.savepoints

    @staticmethod
    async def registrar_batch(operacion, *args, lock=Lock.PESIMISTA, **kwargs):
        uow = await unidad_de_trabajo_async()
        await uow.registrar_batch_async(operacion, *args, lock=lock, **kwargs)