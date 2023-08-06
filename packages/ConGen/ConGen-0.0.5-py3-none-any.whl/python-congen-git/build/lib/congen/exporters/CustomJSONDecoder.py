from json import JSONDecoder
from pydoc import locate


"""
Decode JSON and create Python object instances as an alternative to JSONpickle. This is not used at the moment.
"""
class MyJSONDecoder(JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.from_dict)

    def from_dict(self, d):
        print(f"Decoding {d}")
        if "__class__" in d:
            object = locate(d.get("__class__"))(d.get("value"))
        else:
            object = d
        print(f"Decoded object {object} with type {type(object)}")
        return object