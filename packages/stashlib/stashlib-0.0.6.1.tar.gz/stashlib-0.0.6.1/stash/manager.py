from __future__ import absolute_import

from stash import defaults
from stash.codecs.codec import Codec
from stash.options import StashOptions
from stash.serializers.default import DefaultSerializer
from stash.serializers.serializer import Serializer
from stash.storages.storage import Storage
from stash.utils.checksum import calcsum, to_bytes


class StashManager(object):
    def __init__(
        self,
        storage: Storage,
        codec: Codec,
        options: StashOptions,
        serializer: Serializer = DefaultSerializer(),
    ):
        self.__storage = storage
        self.__codec = codec
        self.__options = options
        self.__serializer = serializer

    def __get_cache_key(self, data):
        return calcsum(data, self.__options.algo)

    def __encode(self, data):
        data = to_bytes(data)
        return self.__codec.encode(data) if self.__codec else data

    def __decode(self, data):
        return self.__codec.decode(data) if self.__codec else data

    def exists(self, key: str) -> bool:
        return self.__storage.exists(self.__get_cache_key(key))

    def purge(self, cutoff: int = defaults.CACHE_MAX_AGE):
        return self.__storage.purge(cutoff)

    def clear(self):
        return self.__storage.clear()

    def close(self):
        return self.__storage.close()

    def write(self, key: str, content):
        data = self.__encode(content)
        return self.__storage.write(self.__get_cache_key(key), data)

    def read(self, key: str):
        data = self.__storage.read(self.__get_cache_key(key))
        if data:
            return self.__decode(data)
        return None

    def rm(self, key: str):
        self.__storage.rm(self.__get_cache_key(key))
