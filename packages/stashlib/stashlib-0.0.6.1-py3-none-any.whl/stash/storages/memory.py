from stash.options import StashOptions
from stash.storages.storage import Storage


class MemoryStorage(Storage):
    def __init__(self, options: StashOptions):
        super().__init__(options)
        self.__dict = {}

    def exists(self, key: str) -> bool:
        return key in self.__dict

    def purge(self, cutoff: int):
        pass

    def clear(self):
        self.__dict.clear()

    def close(self):
        self.clear()

    def write(self, key: str, content):
        self.__dict[key] = content

    def read(self, key: str):
        return self.__dict.get(key)

    def rm(self, key: str):
        self.__dict.pop(key, None)
