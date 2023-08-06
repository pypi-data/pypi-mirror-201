from stash.serializers.serializer import Serializer

try:
    from json import loads, dumps
except ImportError:
    pass


class JSONSerializer(Serializer):
    def deserialize(self, data):
        return loads(data)

    def serialize(self, data):
        return dumps(data)
