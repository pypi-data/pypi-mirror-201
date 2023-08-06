from stash import consts, defaults

_default = {
    "algo": defaults.CACHE_DEFAULT_ALGORITHM,
    "cache_max_age": consts.SECONDS_IN_DAY,
    "cache_min_size": consts.SIZE_KB * 4,
    "fs_cache_filename": defaults.CACHE_DEFAULT_FILENAME,
    "fs_cache_dir": defaults.CACHE_DEFAULT_PATH,
    "fs_cache_dir_level": defaults.CACHE_DEFAULT_DIR_LEVEL,
    "fs_cache_segment_size": defaults.CACHE_SEGMENT_SIZE,
    "fs_cache_file_ext": "",
    "logger": None,
    "lmdb_map_size": consts.SIZE_MB * 4,
    "lmdb_filename": defaults.CACHE_DEFAULT_FILENAME,
    "dbm_filename": defaults.CACHE_DEFAULT_FILENAME + ".dbm",
    "lsmdb_filename": defaults.CACHE_DEFAULT_FILENAME + ".ldb",
    "redis_unix_socket_path": None,
    "redis_host": "localhost",
    "redis_port": 6379,
    "redis_db": 0,
    "redis_ssl": False,
    "redis_ssl_ca_certs": None,
}


class StashOptions(object):
    def __init__(self, data=None):
        if data is None:
            data = _default
        else:
            data |= _default
        super().__setattr__("data", {})
        self.data = data

    def __getattr__(self, name):
        if name in self.data:
            return self.data[name]
        return None

    def __setattr__(self, key, value):
        if key in self.data:
            self.data[key] = value
        else:
            super().__setattr__(key, value)
