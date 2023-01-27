from tph_lang.interpreter.structures import ArrayGroup
from tph_lang.core import LiteralS
from tph_lang.interpreter.structures import (
    OperType1,
    OperType2,
    OperType3,
    OperType4,
    OperType5
)


class EndProgram(OperType1):
    def __call__(self, array, **kwargs):
        return "EOF"


class Input(OperType1):
    @staticmethod
    def is_str(data: str):
        return True if data.startswith("\"") and data.endswith("\"") else False

    @staticmethod
    def is_numeric(data: str):
        if data.isnumeric():
            return True
        try:
            float(data)
        except ValueError as e:
            return False
        else:
            return True

    def to_numeric(self, data: str):
        try:
            value = int(data)
        except ValueError:
            try:
                value = float(data)
            except ValueError:
                return data
            else:
                return value
        else:
            return value

    def __call__(self, array: ArrayGroup, **kwargs):
        data = input(": ")
        if self.is_str(data):
            array.main.append(data)
        else:
            words = data.split(" ")
            for k in words:
                array.main.append(self.to_numeric(k))
        return array


class Output(OperType1):
    def __call__(self, array: ArrayGroup, **kwargs):
        print(*array.main)
        return array


class SimpleSum(OperType1):
    def __call__(self, array: ArrayGroup, **kwargs):
        types = set([type(k) for k in array.main])
        if len(types) == 1:
            if int in types or float in types:
                array.main = sum(array.main)
                return array
            if str in types:
                array.main = "".join(array.main)
                return array
        else:
            raise NotImplemented(f"{self.__class__.__name__} not implemented for multiple types.")
        return array


class IotaRange(OperType5):
    def __call__(self, *args, **kwargs):
        pass
