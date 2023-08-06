from stash.codecs.codec import Codec


class PassthruCodec(Codec):
    def encode(self, data):
        return data

    def decode(self, data):
        return data
