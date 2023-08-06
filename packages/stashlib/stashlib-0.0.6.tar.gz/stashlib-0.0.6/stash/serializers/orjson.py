from stash.serializers.serializer import Serializer

try:
    from orjson import loads, dumps
except ImportError:
    pass


class OrJSONSerializer(Serializer):
    def deserialize(self, data):
        return loads(data)

    def serialize(self, data):
        return dumps(data)
