import zlib
from stash.codecs.codec import Codec


class ZlibCodec(Codec):
    def encode(self, data):
        return zlib.compress(data)

    def decode(self, data):
        return zlib.decompress(data)
