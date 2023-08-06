from stash.codecs.codec import Codec

try:
    import zstd
except ImportError:
    pass


class ZstdCodec(Codec):
    def encode(self, data, level=10):
        return zstd.compress(data, level)

    def decode(self, data):
        return zstd.decompress(data)
