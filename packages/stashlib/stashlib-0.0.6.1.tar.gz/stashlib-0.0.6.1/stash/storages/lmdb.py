try:
    import lmdb
except ImportError:
    pass

from stash.options import StashOptions
from stash.storages.storage import Storage
from stash.utils.checksum import to_bytes


class LmdbStorage(Storage):
    def __init__(self, options: StashOptions):
        super().__init__(options)
        self.__cache_max_age = self.options.cache_max_age
        self._logger = self.options.logger
        self._env = lmdb.open(
            self.options.fs_cache_dir, max_dbs=1, map_size=self.options.lmdb_map_size
        )
        self._db = self._env.open_db(
            self.normalize_string(self.options.fs_cache_filename)
        )

    def exists(self, key: str) -> bool:
        key = key.encode("utf-8")
        with self._env.begin(db=self._db) as txn:
            for k, _ in txn.cursor():
                if k == key:
                    return True

        return False

    def purge(self, cutoff: int):
        pass

    @staticmethod
    def normalize_string(key: str) -> bytes:
        return to_bytes(key.strip())

    def clear(self):
        with self._env.begin(write=True, db=self._db) as txn:
            txn.drop(self._db, delete=False)

    def close(self):
        self._env.close()

    def write(self, key: str, content):
        key = self.normalize_string(key)
        with self._env.begin(write=True, db=self._db) as txn:
            txn.put(key, content)

    def read(self, key: str):
        key = self.normalize_string(key)
        with self._env.begin(db=self._db) as txn:
            return bytes(txn.get(key))

    def rm(self, key: str):
        key = self.normalize_string(key)
        with self._env.begin(write=True, db=self._db) as txn:
            txn.delete(key)
