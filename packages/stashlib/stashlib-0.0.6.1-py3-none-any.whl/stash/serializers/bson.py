from stash.serializers.serializer import Serializer

try:
    from bson import decode, encode
except ImportError:
    pass


class BSONSerializer(Serializer):
    def deserialize(self, data):
        return decode(data)

    def serialize(self, data):
        return encode(data)
