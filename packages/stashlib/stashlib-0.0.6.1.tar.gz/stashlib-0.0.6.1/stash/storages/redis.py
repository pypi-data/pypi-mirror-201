try:
    from redis import Redis
except ImportError:
    pass

from stash.options import StashOptions
from stash.storages.storage import Storage


class RedisStorage(Storage):
    def __init__(self, options: StashOptions):
        super().__init__(options)
        if self.options.redis_unix_socket_path:
            self.client = Redis(unix_socket_path=self.options.redis_unix_socket_path)
        else:
            self.client = Redis(
                host=self.options.redis_host,
                port=self.options.redis_port,
                db=self.options.redis_db,
                ssl=self.options.redis_ssl,
                ssl_ca_certs=self.options.redis_ssl_ca_certs,
            )

    def exists(self, key: str) -> bool:
        return self.client.exists(key) > 0

    def purge(self, cutoff: int):
        pass

    def clear(self):
        self.client.flushdb()

    def close(self):
        self.client.close()

    def write(self, key: str, content):
        # item = {"data": Binary(content), "timestamp": datetime.utcnow()}
        self.client.set(key, content)

    def read(self, key: str):
        return self.client.get(key)

    def rm(self, key: str):
        self.client.delete(key)
