import logging
import traceback

from anonimizador.seedwork.infraestructura.uow import UnidadTrabajo, Batch
from pydispatch import dispatcher

# Instead of using get_db(), we import SessionLocal:
from anonimizador.config.db import Session

class ExcepcionUoW(Exception):
    ...

class UnidadTrabajoSQLAlchemy(UnidadTrabajo):
    """Concrete implementation of UnidadTrabajo using pure SQLAlchemy."""

    def __init__(self):
        # Create a new SQLAlchemy session when this UoW is instantiated.
        self.session = Session
        self._batches: list[Batch] = []
        print(f'Inicializa base de datos con {sizeof(self.batches)} batches')

    def __enter__(self) -> UnidadTrabajo:
        """
        Called when entering a 'with' block:
            with UnidadTrabajoSQLAlchemy() as uow:
                ...
        """
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Called at the end of a 'with' block, whether an exception was raised or not.
        We'll rollback on exception, otherwise commit. Then close the session.
        """
        if exc_type is not None:
            # Something went wrong, so roll back the transaction.
            self.rollback()
        else:
            # Otherwise, commit if everything is fine.
            self.commit()

        # Always close the session when exiting the context.
        self.session.close()

    def _limpiar_batches(self):
        """Reset the list of pending batches."""
        self._batches = []

    @property
    def batches(self) -> list[Batch]:
        return self._batches

    @property
    def savepoints(self) -> list:
        # If you want to implement actual savepoints, do so here.
        return []

    def commit(self, *args, **kwargs):     
        print('######### commit sql alchemy implementation')
        for batch in self.batches:
            # Use batch.lock here if needed for concurrency control.
            batch.operacion(*batch.args, **batch.kwargs)

        # Commit via this UoW's session
        print('######### commiting db changes')
        self.session.commit()

        # Publish post-commit events, then clear the batches
        """Commits the transaction and publishes events post-commit."""
        print("#commit clase base")
        self.batches.clear()
        #self._limpiar_batches()
        #super().commit()

    def rollback(self, savepoint=None):
        """
        Roll back to a given savepoint (if any) or perform a full rollback.
        Then invoke the parent method to potentially handle compensation events.
        """
        if savepoint is not None:
            # If you have logic for real DB savepoints, apply it here.
            savepoint.rollback()
        else:
            self.session.rollback()

        # Let the parent UoW handle compensation events and cleaning
        super().rollback()

    def savepoint(self):
        """Optional: Create a new DB savepoint if your workflow requires it."""
        pass



    def __init__(self):
        self._batches: list[Batch] = list()

    def __enter__(self) -> UnidadTrabajo:
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()

    def _limpiar_batches(self):
        self._batches = list()

    @property
    def savepoints(self) -> list:
        return []

    @property
    def batches(self) -> list[Batch]:
        return self._batches             

    def commit(self):
        index = 0
        try:
            for evento in self._obtener_eventos():
                dispatcher.send(signal=f'{type(evento).__name__}Integracion', evento=evento)
                index += 1
        except:
            logging.error('ERROR: Suscribiendose al tópico de eventos!')
            traceback.print_exc()
            self.rollback(index=index)
        self._limpiar_batches()

    def rollback(self):
        # TODO Implemente la función de rollback
        # Vea los métodos agregar_evento de la clase AgregacionRaiz
        # A cada evento que se agrega, se le asigna un evento de compensación
        # Piense como podría hacer la implementación
        
        super().rollback()
    
    def savepoint(self):
        # NOTE No hay punto de implementar este método debido a la naturaleza de Event Sourcing
        ...