from enum import Enum
from types import DynamicClassAttribute


class AzooBaseEnum(Enum):
    def __eq__(self, target):
        if type(target) in [str, int, float]:
            if type(self.value) == tuple:
                return self.value[0] == target
            return self.value == target

        if isinstance(target, AzooBaseEnum):
            return self is target

    @DynamicClassAttribute
    def val(self):
        """The value of the Enum member."""
        return self._value_[0] if isinstance(self._value_, tuple) else self._value_

    @classmethod
    def list(cls):
        result = []
        for c in cls:
            result.append(c.value if type(c.value) != tuple else c.value[0])
        return result

    @classmethod
    def display(cls, tracking_method):
        for target in cls:
            if type(target.value) == tuple:
                if target.value[0] == tracking_method:
                    return target.value[1]
            else:
                if target == tracking_method:
                    return target.value
        raise ValueError(
            cls.__name__ + ' has no value matching "' + tracking_method + '"'
        )

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]
