from .dataset import HybridDataSet
from pyperspace.config import DataSetConfig, StorageConfig
from pyperspace.workers import DataSetWorkerPool, StorageManagerWorker
from pyperspace.storage import LSMDataSet, StorageManagerClient
from typing import List
import os

class Daemon(DataSetWorkerPool):
    def __init__(self, path: str, ds_cfg: DataSetConfig, sm_cfg: StorageConfig):
        os.makedirs(path, 0o744, exist_ok=True)
        # Start StorageManagerWorker to get the port for DataSetWorkerPool
        self._sm = StorageManagerWorker(path, sm_cfg.cycle_time)
        self._sm.start()
        super().__init__(self._sm.listener_port, \
                         ds_cfg.mode, \
                         path, \
                         ds_cfg.num_nodes, \
                         ds_cfg.insert_buffer_size, \
                         ds_cfg.select_buffer_size, \
                         ds_cfg.freeze_limit, \
                         ds_cfg.acknowledge, \
                         ds_cfg.flush, \
                         ds_cfg.freeze_interval_sec)
        self._sm_client = StorageManagerClient(self._sm.listener_port)

    @property
    def storage(self) -> StorageManagerClient:
        return self._sm_client

    def drop(self, name: str) -> None:
        self._sm_client.drop_dataset(name)
        self.send_drop(name)

    def open_lsm_dataset(self, name: str) -> HybridDataSet:
        return HybridDataSet(self, name, self._sm.listener_port)

    def stop(self) -> None:
        super().stop()
        super().join()
        self._sm_client.close()
        self._sm.stop()
        self._sm.join()

    def close(self) -> None:
        super().close()
        self._sm.close()
