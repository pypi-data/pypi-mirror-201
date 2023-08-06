from stash.serializers.serializer import Serializer

try:
    from simplejson import loads, dumps
except ImportError:
    pass


class SimpleJSONSerializer(Serializer):
    def deserialize(self, data):
        return loads(data)

    def serialize(self, data):
        return dumps(data)
