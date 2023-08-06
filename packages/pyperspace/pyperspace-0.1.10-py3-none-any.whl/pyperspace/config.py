from pyperspace.workers import TCP_MODE, TCP_FAST_MODE, PIPE_MODE

import yaml

_modes = {"tcp" : TCP_MODE,
          "tcp_fast" : TCP_FAST_MODE,
          "pipe" : PIPE_MODE}

class _ConfigBase:
    def _from_kwargs(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

class HTTPConfig(_ConfigBase):
    def __init__(self, **kwargs):
        self.host = "0.0.0.0"
        self.port = 80

        self._from_kwargs(**kwargs)

class DataSetConfig(_ConfigBase):
    def __init__(self, **kwargs):
        self.mode = TCP_MODE
        self.num_nodes = 3
        self.insert_buffer_size = 100
        self.select_buffer_size = 100000
        self.freeze_limit = 5000
        self.acknowledge = False
        self.flush = True
        self.freeze_interval_sec = None

        self._from_kwargs(**kwargs)

class StorageConfig(_ConfigBase):
    def __init__(self, **kwargs):
        self.cycle_time = 5

        self._from_kwargs(**kwargs)

class Config(_ConfigBase):
    def __init__(self, **kwargs):
        self.datasets = DataSetConfig()
        self.storage = StorageConfig()
        self.http = HTTPConfig()
        self.data_dir = "."
        
        self._from_kwargs(**kwargs)

def get_config(filename: str) -> Config:
    with open(filename, 'r') as fd:
        data = yaml.load(fd.read(), Loader=yaml.Loader)
        cfg = Config()

        cfg.data_dir = data['data_dir']
        cfg.datasets.mode = _modes[data['datasets']['mode']]
        cfg.datasets.num_nodes = data['datasets']['num_workers']
        cfg.datasets.insert_buffer_size = data['datasets']['buffers']['insert']
        cfg.datasets.select_buffer_size = data['datasets']['buffers']['select']
        cfg.datasets.freeze_limit = data['datasets']['buffers']['freeze']
        cfg.datasets.acknowledge = data['datasets']['send_acks']
        cfg.datasets.flush = data['datasets']['flush']
        cfg.datasets.freeze_interval_sec = data['datasets']['freeze_interval']
        cfg.storage.cycle_time = data['storage']['compactor']['cycle_secs']
        cfg.http.host = data['http']['host']
        cfg.http.port = data['http']['port']

        return cfg
