from stash.storages.storage import Storage


class NullStorage(Storage):
    def exists(self, key: str) -> bool:
        return False

    def purge(self, cutoff: int):
        pass

    def clear(self):
        pass

    def close(self):
        pass

    def write(self, key: str, content):
        pass

    def read(self, key: str):
        pass

    def rm(self, key: str):
        pass
