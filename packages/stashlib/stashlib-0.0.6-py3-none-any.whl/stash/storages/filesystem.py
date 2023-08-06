import errno
import os
import shutil
import time
from stat import S_ISREG

from stash.options import StashOptions
from stash.storages.storage import Storage
from stash.utils.nested_path import NestedPathBuilder, walk_files, safe_delete_file


class FileSystemStorage(Storage):
    def __init__(self, options: StashOptions):
        super().__init__(options)
        self.__nested_path_builder = NestedPathBuilder(
            self.options.fs_cache_dir,
            self.options.fs_cache_dir_level,
            self.options.fs_cache_segment_size,
        )

    def resolve_filepath(self, key: str) -> str:
        return self.__nested_path_builder.resolve_path_ext(
            key, self.options.fs_cache_file_ext
        )

    def exists(self, key: str) -> bool:
        fpath = self.resolve_filepath(key)
        bigbang = time.time() - self.options.cache_max_age
        try:
            st = os.stat(fpath)
            # check if the cache file exists
            exists = S_ISREG(st.st_mode) and st.st_size > self.options.cache_min_size
            if exists:
                # check cache freshness
                if st.st_mtime < bigbang:
                    # cache is stale. nuke it
                    if self.options.logger:
                        self.options.logger.debug(
                            "Deleting stale cache item: {} Last modified: {}".format(
                                os.path.basename(fpath), time.ctime(st.st_mtime)
                            )
                        )
                    safe_delete_file(fpath)
                    return False
                # cache file exists and is fresh & valid
                return True
            # cache file is non-existent or invalid
            return False
        except (IOError, OSError) as e:
            if e.errno != errno.ENOENT:
                if self.options.logger:
                    self.options.logger.error(e)
                    import traceback

                    self.options.logger.error(traceback.format_exc())

        return False

    def purge(self, cutoff: int):
        files = walk_files(
            self.options.fs_cache_dir, "*" + self.options.fs_cache_file_ext
        )
        bigbang = time.time() - cutoff
        for fname in files:
            try:
                st = os.stat(fname)
                if S_ISREG(st.st_mode):
                    if st.st_mtime < bigbang:
                        safe_delete_file(fname)
            except (IOError, OSError) as e:
                if e.errno != errno.ENOENT:
                    if self.options.logger:
                        self.options.logger.error(e)
                        import traceback

                        self.options.logger.error(traceback.format_exc())

    def clear(self):
        try:
            shutil.rmtree(self.options.fs_cache_dir, ignore_errors=True)
        except (IOError, OSError) as e:
            if e.errno != errno.ENOENT:
                if self.options.logger:
                    self.options.logger.error(e)
                    import traceback

                    self.options.logger.error(traceback.format_exc())

    def close(self):
        pass

    def write(self, key: str, content):
        with open(self.resolve_filepath(key), "wb") as f:
            f.write(content)

    def read(self, key: str):
        with open(self.resolve_filepath(key), "rb") as f:
            return f.read()

    def rm(self, key: str):
        fpath = self.resolve_filepath(key)
        if os.path.isfile(fpath):
            os.unlink(fpath)
