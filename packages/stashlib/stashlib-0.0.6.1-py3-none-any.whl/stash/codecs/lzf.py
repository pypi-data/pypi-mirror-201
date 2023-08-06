from stash.codecs.codec import Codec

try:
    import lzf
except ImportError:
    pass


class LzfCodec(Codec):
    def encode(self, data):
        return lzf.compress(data)

    def decode(self, data):
        return lzf.decompress(data)
