from abc import ABC, abstractmethod
from enum import Enum

from anonimizador.seedwork.dominio.entidades import AgregacionRaiz


from pydispatch import dispatcher

import pickle
import logging
import traceback

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
    """Abstract base class for the Unit of Work."""

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def _obtener_eventos_rollback(self, batches=None):
        batches = self.batches if batches is None else batches
        eventos = []
        for batch in batches:
            for arg in batch.args:
                if isinstance(arg, AgregacionRaiz):
                    eventos += arg.eventos_compensacion
                    break
        return eventos

    def _obtener_eventos(self, batches=None):
        batches = self.batches if batches is None else batches
        eventos = []
        for batch in batches:
            for arg in batch.args:
                if isinstance(arg, AgregacionRaiz):
                    eventos += arg.eventos
                    break
        return eventos

    @abstractmethod
    def _limpiar_batches(self):
        """Clear the list of batches, to be called after commit or rollback."""
        raise NotImplementedError

    @property
    @abstractmethod
    def batches(self) -> list[Batch]:
        """Return the list of current batches."""
        raise NotImplementedError

    @property
    @abstractmethod
    def savepoints(self) -> list:
        """Return the list of current savepoints."""
        raise NotImplementedError

   
    def commit(self):
        """Commits the transaction and publishes events post-commit."""
        print("#commit clase base")
        self._publicar_eventos_dominio()
        self._limpiar_batches()

    @abstractmethod
    def rollback(self, savepoint=None):
        """Rolls back the transaction (or to a specific savepoint)."""
        raise NotImplementedError

    @abstractmethod
    def savepoint(self):
        """Create a new savepoint (if supported)."""
        raise NotImplementedError

    def registrar_batch(self, operacion, *args, lock=Lock.PESIMISTA, **kwargs):
        print(f'utiliza operacion {type(operacion).__name__} --- {operacion}')
        batch = Batch(operacion, lock, *args, **kwargs)
        self.batches.append(batch)

    def _publicar_eventos_dominio(self, batch, repositorio_eventos_func=None):
        """Publish domain events (if you choose to do it prior to commit)."""
        for evento in self._obtener_eventos(batches=[batch]):
            if repositorio_eventos_func:
                repositorio_eventos_func(evento)
            dispatcher.send(signal=f'{type(evento).__name__}Dominio', evento=evento)

    def _publicar_eventos_post_commit(self):
        pass


_current_uow: UnidadTrabajo | None = None

def unidad_de_trabajo() -> UnidadTrabajo:
    """Returns the current active UnidadTrabajo. If none exists,
    you might choose to create a new one or raise an error."""
    global _current_uow
    if _current_uow is None:
        # By default, create a new SQLAlchemy-based UoW if you want:
        from anonimizador.config.uow import UnidadTrabajoSQLAlchemy
        _current_uow = UnidadTrabajoSQLAlchemy()
        print("##creo sql alchemy")
    return _current_uow

def guardar_unidad_trabajo(uow: UnidadTrabajo):
    """Updates the current active UnidadTrabajo."""
    global _current_uow
    _current_uow = uow



class UnidadTrabajoPuerto:
    """Static facade methods to interact with the UoW from other parts of your code."""

    @staticmethod
    def commit():
        uow = unidad_de_trabajo()
        print(f'USING TYPE: {type(uow).__name__}')
        uow.commit()
        print('despues del commit')
        guardar_unidad_trabajo(uow)

    @staticmethod
    def rollback(savepoint=None):
        uow = unidad_de_trabajo()
        uow.rollback(savepoint=savepoint)
        guardar_unidad_trabajo(uow)

    @staticmethod
    def savepoint():
        uow = unidad_de_trabajo()
        uow.savepoint()
        guardar_unidad_trabajo(uow)

    @staticmethod
    def dar_savepoints():
        uow = unidad_de_trabajo()
        return uow.savepoints

    @staticmethod
    def registrar_batch(operacion, *args, lock=Lock.PESIMISTA, **kwargs):
        print("#commit trabajo puerto")
        uow = unidad_de_trabajo()
        uow.registrar_batch(operacion, *args, lock=lock, **kwargs)
        guardar_unidad_trabajo(uow)        