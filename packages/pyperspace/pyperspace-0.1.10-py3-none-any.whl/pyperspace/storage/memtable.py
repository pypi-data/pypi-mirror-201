from pyperspace.data import RawEntry, Entry, FlatTree, filter_deleted
from pyperspace.io import WriteAheadLog, WAL_INSERT, WAL_DELETE

from typing import Iterable

B_EMPTY = b''

class MemTable:
    __slots__ = ('_deletes', '_data_insert', '_data')
    def __init__(self):
        self.clear()

    def delete(self, begin_time: int, end_time: int) -> None:
        _deletes = self._deletes
        for e in self.find_range(begin_time, end_time):
            e.deleted = True
            _deletes += 1
        self._deletes = _deletes

    def load_from_wal(self, wal: WriteAheadLog) -> None:
        _read_one = wal.read_one
        _data_insert = self._data_insert
        _delete = self.delete
        while not wal.eof:
            e_type, data = _read_one()
            if e_type == WAL_INSERT:
                _data_insert(data)
            elif e_type == WAL_DELETE:
                _delete(*data)
            else:
                raise IOError(f"unsupported entry type ({e_type}) decoded from write-ahead log")

    @property
    def count(self) -> int:
        return len(self._data) - self._deletes
    
    def insert_raw(self, e: RawEntry) -> None:
        self._data_insert(e)

    def clear(self) -> None:
        # 2000 was found to be an optimal size after profiling against one Python 3.7 instance
        self._data = FlatTree(2000)
        self._data_insert = self._data.insert
        self._deletes = 0

    def find_range(self, begin_time: int, end_time: int) -> Iterable[Entry]:
        return filter_deleted(self._data.iter_range(Entry(begin_time, B_EMPTY), Entry(end_time, B_EMPTY)))

    def find_all(self) -> Iterable[Entry]:
        return filter_deleted(iter(self._data))

    def __iter__(self) -> Iterable[Entry]:
        return filter_deleted(iter(self._data))

    @property
    def begin_time(self) -> int:
        return self._data.first.time

    @property
    def end_time(self) -> int:
        return self._data.last.time

    @property
    def empty(self) -> bool:
        return self.count == 0
