from stash.serializers.serializer import Serializer

try:
    from msgpack import loads, dumps
except ImportError:
    pass


class MsgPackSerializer(Serializer):
    def deserialize(self, data):
        return loads(data)

    def serialize(self, data):
        return dumps(data)
