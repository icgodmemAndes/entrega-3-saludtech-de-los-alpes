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
        self.lock = lock
        self.kwargs = kwargs

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
                    eventos += arg.eventos_compensacion
                    break
        return eventos

    def _obtener_eventos(self, batches=None):
        batches = self.batches if batches is None else batches
        eventos = list()
        for batch in batches:
            for arg in batch.args:
                if isinstance(arg, AgregacionRaiz):
                    eventos += arg.eventos
                    break
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

    def commit(self):
        self._publicar_eventos_post_commit()
        self._limpiar_batches()

    @abstractmethod
    def rollback(self, savepoint=None):
        self._limpiar_batches()
    
    @abstractmethod
    def savepoint(self):
        raise NotImplementedError

    def registrar_batch(self, operacion, *args, lock=Lock.PESIMISTA, repositorio_eventos_func=None,**kwargs):
        batch = Batch(operacion, lock, *args, **kwargs)
        self.batches.append(batch)
        self._publicar_eventos_dominio(batch, repositorio_eventos_func)

    def _publicar_eventos_dominio(self, batch, repositorio_eventos_func):
        for evento in self._obtener_eventos(batches=[batch]):
            if repositorio_eventos_func:
                repositorio_eventos_func(evento)
            dispatcher.send(signal=f'{type(evento).__name__}Dominio', evento=evento)

    def _publicar_eventos_post_commit(self):
        try:
            for evento in self._obtener_eventos():
                dispatcher.send(signal=f'{type(evento).__name__}Integracion', evento=evento)
        except:
            logging.error('ERROR: Suscribiendose al tópico de eventos!')
            traceback.print_exc()
            

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
    from etiquetado.config.uow import UnidadTrabajoSQLAlchemy, UnidadTrabajoPulsar
    if session.get('uow'):
        return session['uow']

    uow_serialized = pickle.dumps(UnidadTrabajoSQLAlchemy())
    if session.get('uow_metodo') == 'pulsar':
        uow_serialized = pickle.dumps(UnidadTrabajoPulsar())

    registrar_unidad_de_trabajo(uow_serialized)
    return uow_serialized

async def fastapi_uow():
    # Get the request state to store/retrieve UoW
    try:
        from fastapi import Request
        
        # Note: This requires proper request context setup
        request = Request.get_current()
        
        # Check if UoW is already in the request state
        if hasattr(request.state, 'uow'):
            return request.state.uow
        
        # Create a new UnidadTrabajoPulsar and store it in request state
        uow = UnidadTrabajoPulsar()
        request.state.uow = uow
        return uow
    except Exception as e:
        # Fallback if not in request context or other error
        return UnidadTrabajoPulsar()

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
        registrar_unidad_de_trabajo(pickle.dumps(uow))
    else:
        raise Exception('No hay unidad de trabajo')


class UnidadTrabajoPuerto:

    @staticmethod
    def commit():
        uow = unidad_de_trabajo()
        uow.commit()

    @staticmethod
    def rollback(savepoint=None):
        uow = unidad_de_trabajo()
        uow.rollback(savepoint=savepoint)

    @staticmethod
    def savepoint():
        uow = unidad_de_trabajo()
        return uow.savepoint()

    @staticmethod
    def dar_savepoints():
        uow = unidad_de_trabajo()
        return uow.savepoints()
    
    @staticmethod
    def registrar_batch(operacion, *args, lock=Lock.PESIMISTA, **kwargs):
        uow = unidad_de_trabajo()
        return uow.registrar_batch(operacion, *args, lock=lock, **kwargs)

class UnidadTrabajoPuertoAsync:
    """
    Implementación de UnidadTrabajoPuerto para entornos asincrónicos como FastAPI
    """
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
        return await uow.savepoints()
    
    @staticmethod
    async def registrar_batch(operacion, *args, lock=Lock.PESIMISTA, **kwargs):
        uow = await unidad_de_trabajo_async()
        return await uow.registrar_batch_async(operacion, *args, lock=lock, **kwargs)

class UnidadTrabajoPulsar(UnidadTrabajo):
    """
    Implementación de Unit of Work para operaciones asincrónicas en FastAPI
    usando Apache Pulsar para mensajería
    """
    def __init__(self):
        self._batches = []
        self._savepoints = []
        self._pulsar_client = None
    
    async def __aenter__(self):
        """Async context manager support for FastAPI"""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager support for FastAPI"""
        if exc_type:
            await self.rollback()
    
    def _limpiar_batches(self):
        self._batches = []
    
    @property
    def batches(self) -> list[Batch]:
        return self._batches
    
    @property
    def savepoints(self) -> list:
        return self._savepoints
    
    async def commit(self):
        """
        Realiza la confirmación de todos los batches pendientes de forma asincrónica
        y publica los eventos asociados
        """
        try:
            # Ejecutar todas las operaciones de batch
            for batch in self._batches:
                await self._ejecutar_batch_async(batch)
            
            # Publicar eventos post-commit
            await self._publicar_eventos_post_commit_async()
            
            # Limpiar los batches después de completar
            self._limpiar_batches()
        except Exception as e:
            # En caso de error, realizar rollback
            await self.rollback()
            raise e
    
    async def _ejecutar_batch_async(self, batch):
        """
        Ejecuta un batch de operaciones de forma asincrónica
        """
        # Verificar si la operación es asincrónica
        if asyncio.iscoroutinefunction(batch.operacion):
            # Si es async, await directamente
            await batch.operacion(*batch.args, **batch.kwargs)
        else:
            # Si no es async, ejecutar en threadpool
            from starlette.concurrency import run_in_threadpool
            await run_in_threadpool(batch.operacion, *batch.args, **batch.kwargs)
    
    async def rollback(self, savepoint=None):
        """
        Deshace las operaciones realizadas hasta el punto de guardado especificado
        """
        # Implementar lógica de rollback para Apache Pulsar
        if savepoint:
            index = self._savepoints.index(savepoint) if savepoint in self._savepoints else -1
            if index != -1:
                # Revertir hasta el punto de guardado
                self._batches = self._batches[:index]
                self._savepoints = self._savepoints[:index]
        else:
            # Rollback completo
            self._limpiar_batches()
            self._savepoints = []
    
    async def savepoint(self):
        """
        Crea un punto de guardado para poder revertir operaciones posteriormente
        """
        # Crear un identificador único para este savepoint
        savepoint_id = f"sp_{len(self._savepoints)}_{id(self)}"
        self._savepoints.append(savepoint_id)
        return savepoint_id
    
    async def registrar_batch_async(self, operacion, *args, lock=Lock.PESIMISTA, 
                                repositorio_eventos_func=None, **kwargs):
        """
        Registra un batch de operaciones de forma asincrónica
        """
        batch = Batch(operacion, lock, *args, **kwargs)
        self._batches.append(batch)
        await self._publicar_eventos_dominio_async(batch, repositorio_eventos_func)
    
    async def _publicar_eventos_dominio_async(self, batch, repositorio_eventos_func):
        """
        Publica eventos de dominio de forma asincrónica
        """
        eventos = self._obtener_eventos(batches=[batch])
        for evento in eventos:
            if repositorio_eventos_func:
                if asyncio.iscoroutinefunction(repositorio_eventos_func):
                    await repositorio_eventos_func(evento)
                else:
                    from starlette.concurrency import run_in_threadpool
                    await run_in_threadpool(repositorio_eventos_func, evento)
            
            # Usar dispatcher de forma sincrónica (puede necesitar adaptación para async)
            dispatcher.send(signal=f'{type(evento).__name__}Dominio', evento=evento)
    
    async def _publicar_eventos_post_commit_async(self):
        """
        Publica eventos de integración después del commit de forma asincrónica
        """
        try:
            eventos = self._obtener_eventos()
            for evento in eventos:
                # Publicar eventos usando dispatcher
                dispatcher.send(signal=f'{type(evento).__name__}Integracion', evento=evento)
                
                # Si se ha configurado el cliente de Pulsar
                if self._pulsar_client:
                    # Implementar aquí la lógica para publicar en Pulsar
                    # Ejemplo pseudocódigo:
                    # producer = await self._pulsar_client.create_producer(
                    #    f'eventos-{type(evento).__name__}')
                    # await producer.send(pickle.dumps(evento))
                    pass
                    
        except Exception as e:
            logging.error('ERROR: Publicando eventos en Pulsar!')
            traceback.print_exc()