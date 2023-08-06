import json
import os
from collections import namedtuple


def get_json_string(self, path: str):
    if not os.path.exists(path):
        raise "File not found. " + path

    f = open(path, "r", encoding='utf-8-sig')
    t = f.read()
    f.close()
    return t


def to_json(self, obj: object):
    return json.dumps(obj=obj)


def from_json(self, path_or_json: str):
    if os.path.exists(path_or_json):
        path_or_json = self.get_json_string(path_or_json)
    return json.loads(path_or_json)


def __json_object_hook(self, d):
    return namedtuple('X', d.keys())(*d.values())


def json2obj(self, data: str):
    if os.path.exists(data):
        data = self.get_json_string(data)
    return json.loads(data, object_hook=self.__json_object_hook)


# cls = JsonConverter()

# r = cls.to_json({"x": "yxs"})
# print(r)

# x = cls.from_json(r)
# print(x)
