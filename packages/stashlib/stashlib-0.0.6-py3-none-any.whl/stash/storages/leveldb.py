from stash.storages.storage import Storage


class LeveldbStorage(Storage):
    def close(self):
        pass

    def exists(self, key: str) -> bool:
        pass

    def purge(self, cutoff: int):
        pass

    def clear(self):
        pass

    def write(self, key: str, content):
        pass

    def read(self, key: str):
        pass

    def rm(self, key: str):
        pass
