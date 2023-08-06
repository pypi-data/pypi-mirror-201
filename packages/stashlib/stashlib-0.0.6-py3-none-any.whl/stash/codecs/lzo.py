from stash.codecs.codec import Codec

try:
    import lzo
except ImportError:
    pass


class LzoCodec(Codec):
    def encode(self, data):
        return lzo.compress(data)

    def decode(self, data):
        return lzo.decompress(data)
