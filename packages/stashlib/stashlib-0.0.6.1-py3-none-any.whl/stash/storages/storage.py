from abc import ABC, abstractmethod

from stash.options import StashOptions


class Storage(ABC):
    def __init__(self, options: StashOptions):
        self.options = options

    @abstractmethod
    def exists(self, key: str) -> bool:
        return False

    @abstractmethod
    def purge(self, cutoff: int):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def write(self, key: str, content):
        pass

    @abstractmethod
    def read(self, key: str):
        pass

    @abstractmethod
    def rm(self, key: str):
        pass
