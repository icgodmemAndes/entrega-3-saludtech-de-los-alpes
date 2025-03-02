from anonimizador.seedwork.infraestructura.uow import UnidadTrabajo, Lock, Batch
from anonimizador.seedwork.dominio.entidades import AgregacionRaiz
from pydispatch import dispatcher
import logging
import traceback

from anonimizador.seedwork.infraestructura.uow_async import UnidadTrabajoAsync

class UnidadTrabajoAsync(UnidadTrabajo):
    def __init__(self):
        self._batches = []
        self._savepoints = []

    def _limpiar_batches(self):
        self._batches = []

    def batches(self) -> list[Batch]:
        return self._batches

    def savepoints(self) -> list:
        return self._savepoints

    async def commit(self):
        self._publicar_eventos_post_commit()
        self._limpiar_batches()

    async def rollback(self, savepoint=None):
        self._limpiar_batches()

    async def savepoint(self):
        self._savepoints.append(self._batches.copy())

    async def registrar_batch(self, operacion, *args, lock=Lock.PESIMISTA, repositorio_eventos_func=None, **kwargs):
        batch = Batch(operacion, lock, *args, **kwargs)
        self._batches.append(batch)
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
            logging.error('ERROR: Publicando eventos post commit!')
            traceback.print_exc()




class UnidadTrabajoPuerto:

    @staticmethod
    async def commit():
        uow = UnidadTrabajoAsync()
        await uow.commit()

    @staticmethod
    async def rollback(savepoint=None):
        uow = UnidadTrabajoAsync()
        await uow.rollback(savepoint=savepoint)

    @staticmethod
    async def savepoint():
        uow = UnidadTrabajoAsync()
        await uow.savepoint()

    @staticmethod
    async def dar_savepoints():
        uow = UnidadTrabajoAsync()
        return uow.savepoints()

    @staticmethod
    async def registrar_batch(operacion, *args, lock=Lock.PESIMISTA, **kwargs):
        uow = UnidadTrabajoAsync()
        await uow.registrar_batch(operacion, *args, lock=lock, **kwargs)