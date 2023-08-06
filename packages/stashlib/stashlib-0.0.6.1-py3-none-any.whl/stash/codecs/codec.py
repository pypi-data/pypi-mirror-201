from abc import ABC, abstractmethod


class Codec(ABC):
    @abstractmethod
    def encode(self, data):
        pass

    @abstractmethod
    def decode(self, data: bytes):
        pass
