import json
from ctypes import Array
from typing import Any

from kindenty.base.OrmField import Field


class DtoType:

    def __init__(self, objType):
        self.type = objType


class ObjType(DtoType):

    def __init__(self, objType):
        super(ObjType, self).__init__(objType)


class ListType(DtoType):

    def __init__(self, objType):
        super(ListType, self).__init__(objType)


class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if cls.__name__ == 'BaseModel':
            return type.__new__(cls, name, bases, attrs)
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, (Field, DtoType)):
                mappings[k] = v
        for k in mappings.keys():
            attrs.pop(k)

        attrs['__mappings__'] = mappings
        return type.__new__(cls, name, bases, attrs)


class BaseModel(dict, metaclass=ModelMetaclass):

    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)

    def __getattr__(self, key) -> Any:
        return self.get(key, None)

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value

    def setAttrs(self, keys: (list, tuple, Array), values: (list, tuple)):
        mappings = self.__mappings__
        for i in range(len(keys)):
            if keys[i] in mappings.keys():
                self[keys[i]] = mappings[keys[i]].parseToObj(values[i])
            else:
                self[keys[i]] = values[i]
        return self

    def decode(self, s):
        d = json.loads(s)
        obj = typeToObj(self.__class__, d)
        return obj

    def dict2Obj(self, d):
        for k, v in d.items():
            dtoT = self.__mappings__.get(k, None)
            if isinstance(dtoT, ObjType):
                if isinstance(v, str):
                    v = json.loads(v)
                obj = dtoT.type()
                setattr(self, k, obj.dict2Obj(v))
            elif isinstance(dtoT, ListType):
                if isinstance(v, str):
                    v = json.loads(v)
                obj = dtoT.type()
                setattr(self, k, list(map(obj.dict2Obj, v)))
            else:
                setattr(self, k, v)


def typeToObj(type,d):
    obj = type()
    for k, v in d.items():
        dtoT = type.__mappings__.get(k, None)
        if isinstance(dtoT, ObjType):
            if isinstance(v, str):
                v = json.loads(v)
            obj = dtoT.type()
            setattr(obj, k, obj.dict2Obj(v))
        elif isinstance(dtoT, ListType):
            if isinstance(v, str):
                v = json.loads(v)
            setattr(obj, k, list(map(lambda o: typeToObj(dtoT.type,o), v)))
        else:
            setattr(obj, k, v)
    return obj