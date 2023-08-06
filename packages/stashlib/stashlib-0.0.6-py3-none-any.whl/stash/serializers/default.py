from stash.serializers.serializer import Serializer
import pickle


class DefaultSerializer(Serializer):
    def deserialize(self, data):
        return pickle.loads(data)

    def serialize(self, data):
        return pickle.dumps(data)
