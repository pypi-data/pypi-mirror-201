from stash.serializers.serializer import Serializer

try:
    from cbor2 import dumps, loads
except ImportError:
    pass


class CBORSerializer(Serializer):
    def deserialize(self, data):
        return loads(data)

    def serialize(self, data):
        return dumps(data)
