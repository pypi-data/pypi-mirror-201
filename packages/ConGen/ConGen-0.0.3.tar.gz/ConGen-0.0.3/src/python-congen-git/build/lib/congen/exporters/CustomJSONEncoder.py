from json import JSONEncoder
from typing import Any


"""
Encode JSON from Python object instances as an alternative to JSONpickle. This is not used at the moment.
"""
class MyJSONEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        print(f"Encoding {o}: {type(o)}")
        if hasattr(o, "toJSON"):
            value = o.toJSON()
        elif isinstance(o, type):
            value = str(o)
        else:
            value = super().default(o)

        return {
            "__class__": f"{o.__module__}.{o.__class__.__qualname__}",
            "value": value
        }