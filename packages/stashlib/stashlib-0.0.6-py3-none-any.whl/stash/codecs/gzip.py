from stash.codecs.codec import Codec

try:
    import gzip
except ImportError:
    pass


class GZipCodec(Codec):
    def encode(self, data):
        return gzip.compress(data)

    def decode(self, data):
        return gzip.decompress(data)
