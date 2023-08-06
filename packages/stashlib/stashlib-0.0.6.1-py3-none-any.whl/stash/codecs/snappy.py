from stash.codecs.codec import Codec

try:
    import snappy
except ImportError:
    pass


class SnappyCodec(Codec):
    def encode(self, data):
        return snappy.compress(data)

    def decode(self, data):
        return snappy.uncompress(data)
