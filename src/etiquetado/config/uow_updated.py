from enum import Enum

from etiquetado.seedwork.infraestructura.uow import UnidadTrabajo, Batch, Lock
from etiquetado.config.db_updated import get_db_session

class ExcepcionUoW(Exception):
    pass

class UnidadTrabajoSQLAlchemy(UnidadTrabajo):

    def __init__(self):
        self._batches = []
        self._savepoints = []
        self._session = None

    def __enter__(self) -> UnidadTrabajo:
        self._session = get_db_session()
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()
        self._session.close()

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

    def commit(self):
        try:
            for batch in self._batches:
                batch.operacion(*batch.args, **batch.kwargs)
            self._session.commit()

            self._publicar_eventos_post_commit()
            self._limpiar_batches()
        except Exception as e:
            self.rollback()
            raise ExcepcionUoW(f"Error en commit: {str(e)}")

    def rollback(self, savepoint=None):
        try:
            # No utilizamos el savepoint SQL de la BD pues no nos permite manipular los batches
            # Simplemente vamos removiendo todos los batches posteriores al savepoint seleccionado

            if savepoint:
                self._session.rollback()

                index = 0
                for i, sp in enumerate(self._savepoints):
                    if sp == savepoint:
                        index = i
                        break
                
                self._batches = self._batches[:index]
                self._savepoints = self._savepoints[:index]
            else:
                self._session.rollback()
                self._limpiar_batches()
        except Exception as e:
            raise ExcepcionUoW(f"Error en rollback: {str(e)}")