from stash.codecs.codec import Codec

try:
    import brotli
except ImportError:
    pass


class BrotliCodec(Codec):
    def encode(self, data):
        return brotli.compress(data)

    def decode(self, data):
        return brotli.decompress(data)
