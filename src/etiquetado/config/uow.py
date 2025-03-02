from enum import Enum

from etiquetado.seedwork.infraestructura.uow import UnidadTrabajo, Batch, Lock
from etiquetado.config.db import get_db_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
class ExcepcionUoW(Exception):
    pass

class UnidadTrabajoSQLAlchemy(UnidadTrabajo):

    def __init__(self):
        self._batches = []
        self._savepoints = []
        self._engine = None

    def __enter__(self) -> UnidadTrabajo:
        self._engine = get_db_engine()
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()
        #self._session.close()

    def _limpiar_batches(self):
        self._batches = []

    def savepoints(self) -> list:
        return self._savepoints

    def savepoint(self):
        sp_name = f'sp_{len(self._savepoints)}'
        self._savepoints.append(sp_name)
        return sp_name

    def batches(self) -> list[Batch]:
        return self._batches

    async def commit(self):
        try:
            for batch in self._batches:
                batch.operacion(*batch.args, **batch.kwargs)
            async with AsyncSession(self._engine) as session:
                async with session.begin():
                    await session.commit()

            self._publicar_eventos_post_commit()
            self._limpiar_batches()
        except Exception as e:
            self.rollback()
            raise ExcepcionUoW(f"Error en commit: {str(e)}")

    async def rollback(self, savepoint=None):
        try:
            # No utilizamos el savepoint SQL de la BD pues no nos permite manipular los batches
            # Simplemente vamos removiendo todos los batches posteriores al savepoint seleccionado

            if savepoint:
                async with AsyncSession(self._engine) as session:
                    async with session.begin():
                        self.session.rollback()

                index = 0
                for i, sp in enumerate(self._savepoints):
                    if sp == savepoint:
                        index = i
                        break
                
                self._batches = self._batches[:index]
                self._savepoints = self._savepoints[:index]
            else:
                async with AsyncSession(self._engine) as session:
                    async with session.begin():
                        self.session.rollback()
                self._limpiar_batches()
        except Exception as e:
            raise ExcepcionUoW(f"Error en rollback: {str(e)}")

    # Async support for FastAPI
    async def commit_async(self):
        """Async version of commit for FastAPI"""
        from starlette.concurrency import run_in_threadpool
        await run_in_threadpool(self.commit)

    async def rollback_async(self, savepoint=None):
        """Async version of rollback for FastAPI"""
        from starlette.concurrency import run_in_threadpool
        await run_in_threadpool(lambda: self.rollback(savepoint))

    async def savepoint_async(self):
        """Async version of savepoint for FastAPI"""
        from starlette.concurrency import run_in_threadpool
        return await run_in_threadpool(self.savepoint)

    async def registrar_batch_async(self, operacion, *args, lock=Lock.PESIMISTA, **kwargs):
        """Async version of registrar_batch for FastAPI"""
        from starlette.concurrency import run_in_threadpool
        batch = Batch(operacion, lock, *args, **kwargs)
        self._batches.append(batch)
        # No events for now - simplify for async