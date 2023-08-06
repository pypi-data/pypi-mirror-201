import errno
import fnmatch
import os


def split_segments(s: str, level: int, segment_size: int) -> list:
    segments = [
        s[i : i + segment_size]
        for i in range(1, 1 + (segment_size * level), segment_size)
    ]
    segments.append(s[1 + (segment_size * level) :])
    return segments


def mkdir_p(path: str):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def safe_delete_file(fname: str):
    try:
        os.unlink(fname)
    except:
        pass


def walk_files(folder: str, pattern: str):
    matches = []
    for root, dirnames, filenames in os.walk(folder):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches


class NestedPathBuilder(object):
    def __init__(self, base_dir: str, dir_level: int, segment_size: int):
        self.__base_dir = base_dir
        self.dir_level = dir_level
        self.segment_size = segment_size

    def __resolve_dir_path(self, key: str) -> tuple:
        if not os.path.exists(self.__base_dir):
            mkdir_p(self.__base_dir)
        path = os.sep.join(split_segments(key, self.dir_level, self.segment_size))
        path = os.path.abspath(os.path.join(self.__base_dir, path))
        dirname = os.path.dirname(path)
        mkdir_p(dirname)
        return dirname, path

    def resolve_path(self, key: str) -> str:
        _, path = self.__resolve_dir_path(key)
        return path

    def resolve_dir(self, key: str) -> str:
        dirname, _ = self.__resolve_dir_path(key)
        return dirname

    def resolve_path_ext(self, key: str, suffix: str = None) -> str:
        # return os.path.join(self.resolve_dir(key), key + suffix if suffix else key)
        path = self.resolve_path(key)
        return path + suffix if suffix else path
