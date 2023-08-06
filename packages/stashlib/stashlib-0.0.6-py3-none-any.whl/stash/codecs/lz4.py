from stash.codecs.codec import Codec

try:
    import lz4.frame
except ImportError:
    pass


class Lz4Codec(Codec):
    def encode(self, data):
        return lz4.frame.compress(data)

    def decode(self, data):
        return lz4.frame.decompress(data)
