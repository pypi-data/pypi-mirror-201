import os
from time import time
import dbm
from stash.options import StashOptions
from stash.storages.storage import Storage


class DbmStorage(Storage):
    def __init__(self, options: StashOptions):
        super().__init__(options)
        dbpath = os.path.join(self.options.fs_cache_dir, options.dbm_filename)
        self.__db = dbm.open(dbpath, "c")

    def _data_key(self, key: str) -> str:
        return f"{key.strip()}^@d"

    def _meta_key(self, key: str) -> str:
        return f"{key.strip()}^@m"

    def exists(self, key: str) -> bool:
        # if self._meta_key(key) not in self.__db.keys(): return False
        return self._data_key(key) in self.__db.keys()

    def purge(self, cutoff: int):
        pass

    def clear(self):
        self.__db.clear()

    def close(self):
        self.__db.close()

    def write(self, key: str, content):
        self.__db[self._data_key(key)] = content
        self.__db[self._meta_key(key)] = str(time())

    def read(self, key: str):
        return self.__db.get(self._data_key(key))

    def rm(self, key: str):
        self.__db.pop(key)
