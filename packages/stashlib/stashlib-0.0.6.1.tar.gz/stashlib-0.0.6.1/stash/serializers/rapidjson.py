from stash.serializers.serializer import Serializer

try:
    from rapidjson import loads, dumps
except ImportError:
    pass


class RapidJSONSerializer(Serializer):
    def deserialize(self, data):
        return loads(data)

    def serialize(self, data):
        return dumps(data)
