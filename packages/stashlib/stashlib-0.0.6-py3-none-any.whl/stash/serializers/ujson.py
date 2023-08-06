from stash.serializers.serializer import Serializer

try:
    from ujson import loads, dumps
except ImportError:
    pass


class UltraJSONSerializer(Serializer):
    def deserialize(self, data):
        return loads(data)

    def serialize(self, data):
        return dumps(data)
