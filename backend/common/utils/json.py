import json


class DataEncoder(json.JSONEncoder):
    EMPTY_STRING = ""

    def _encode(self, obj):
        if isinstance(obj, dict):
            return {
                key: (
                    self._encode(value)
                    if self._encode(value) is not None
                    else self.EMPTY_STRING
                )
                for key, value in obj.items()
            }

        return obj

    def encode(self, obj):
        return super(DataEncoder, self).encode(self._encode(obj))
