from etiquetado.config.db import db
from etiquetado.seedwork.infraestructura.uow import UnidadTrabajo, Batch

import logging
import traceback

class ExcepcionUoW(Exception):
    ...

class UnidadTrabajoSQLAlchemy(UnidadTrabajo):

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
        # TODO Lea savepoint
        return []

    @property
    def batches(self) -> list[Batch]:
        return self._batches             

    def commit(self):
        for batch in self.batches:
            lock = batch.lock
            batch.operacion(*batch.args, **batch.kwargs)
                
        db.session.commit() # Commits the transaction

        super().commit()

    def rollback(self, savepoint=None):
        if savepoint:
            savepoint.rollback()
        else:
            db.session.rollback()
        
        super().rollback()
    
    def savepoint(self):
        # TODO Con MySQL y Postgres se debe usar el with para tener la lógica del savepoint
        # Piense como podría lograr esto ¿tal vez teniendo una lista de savepoints y momentos en el tiempo?
        ...


class UnidadTrabajoPulsar(UnidadTrabajo):
    def __init__(self):
        self.client = pulsar.Client('pulsar://localhost:6650')  # Change if needed
        self.producer = self.client.create_producer('persistencia_eventos')
        self.batches_list = []
        self.savepoints_list = []

    async def _publicar_eventos_pulsar(self, eventos):
        for evento in eventos:
            try:
                self.producer.send_async(str(evento).encode('utf-8'), callback=None)
            except Exception as e:
                print(f"Error sending event to Pulsar: {e}")

    async def commit(self):
        eventos = self._obtener_eventos()
        await self._publicar_eventos_pulsar(eventos)
        self._limpiar_batches()

    async def rollback(self, savepoint=None):
        if savepoint and savepoint in self.savepoints_list:
            index = self.savepoints_list.index(savepoint)
            self.batches_list = self.batches_list[:index]
            self.savepoints_list = self.savepoints_list[:index]
        else:
            self._limpiar_batches()

    async def savepoint(self):
        savepoint = f"sp_{len(self.savepoints_list)}"
        self.savepoints_list.append(savepoint)
        return savepoint

    def savepoints(self) -> list:
        return self.savepoints_list

    def _limpiar_batches(self):
        self.batches_list = []

    def batches(self) -> list:
        return self.batches_list

    def registrar_batch(self, operacion, *args, lock=Lock.PESIMISTA, **kwargs):
        batch = Batch(operacion, lock, *args, **kwargs)
        self.batches_list.append(batch)