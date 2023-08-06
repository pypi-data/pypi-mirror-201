from stash.codecs.codec import Codec

try:
    import lzma
except ImportError:
    try:
        import backports.lzma as lzma
    except ImportError:
        pass


class LzmaCodec(Codec):
    def encode(self, data):
        return lzma.compress(data)

    def decode(self, data):
        return lzma.decompress(data)
