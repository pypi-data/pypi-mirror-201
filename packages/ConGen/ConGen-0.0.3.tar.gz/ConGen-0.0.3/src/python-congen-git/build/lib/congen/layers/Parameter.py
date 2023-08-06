import sys


class TypeDefaults(dict):
    def __init__(self, default, min, max):
        super().__init__(default = default, min = min, max = max)


class Parameter(dict):
    parameterDefaults = {
        str: TypeDefaults("N/A", None, None),
        int: TypeDefaults(0, -(sys.maxsize-1), sys.maxsize),
        float: TypeDefaults(0.0, sys.float_info.min, sys.float_info.max),
        bool: TypeDefaults(False, None, None),
        "default": TypeDefaults(None, None, None)
    }
    def __init__(self, name = "New Parameter", desc = "A new Parameter", parameterType = str, invalidates_cache = False,
                **kwargs):
        super().__init__(name=name, desc=desc, parameterType=parameterType, invalidates_cache=invalidates_cache, **kwargs)

        try:
            for attr_name in ["default", "min", "max"]:
                self[attr_name] = \
                    kwargs[attr_name] if attr_name in kwargs \
                    else self.parameterDefaults[parameterType][attr_name] if parameterType in self.parameterDefaults \
                    else self.parameterDefaults["default"][attr_name]
        except KeyError:
            raise ValueError(f"Class Parameter is not defined for parameterType {parameterType.__name__}")

        self.value = kwargs["value"] if "value" in kwargs else self.default

    def __str__(self):
        return f"{self.name}: {self.value}"

    __delattr__ = dict.__delitem__

    def __setattr__(self, key, value):
        if self.parameterType is congen.layers.Layer.Layer and key == "value" and value is not None:
            # Now store the Layer id instead of the layer itself for easier de-pickling with jsonpickle
            value = congen.LayerListCtrl.LayerListCtrl.current_instance.layer_list.index(value)
        return self.__setitem__(key, value) # Method inherited from dict

    def __getattr__(self, item):
        if self.get("parameterType") is congen.layers.Layer.Layer and item == "value":
            if self.get(item) is not None and self.get(item) < len(congen.LayerListCtrl.LayerListCtrl.current_instance.layer_list):
                # Now return the Layer itself instead of the layer id itself for easier de-pickling with jsonpickle
                return congen.LayerListCtrl.LayerListCtrl.current_instance.layer_list[self.get(item)]
            else:
                return None
        elif item in self:
            return self.get(item) # Method inherited from dict
        else:
            raise AttributeError(f"{self.__class__.__name__} has no attribute {item}.")

    def toJSON(self):
        print("toJSON of Parameter called!")
        json_dict = self.__dict__.copy()
        json_dict["parameterType"] = str(self["parameterType"])
        return json_dict

    def __setstate__(self, state):
        print(f"De-pickling Parameter {state}")
        self.__dict__.update(state)

class ParameterDict(dict):
    def __init__(self, parameter_list = None):
        super().__init__()
        self.cache_invalidators = list()
        self.extend(parameter_list)

    def append(self, parameter):
        super().update({parameter.name: parameter})
        if parameter.invalidates_cache:
            self.cache_invalidators.append(parameter.name)

    def extend(self, parameter_list):
        if parameter_list != None:
            for parameter in parameter_list:
                self.append(parameter)

    def get_ids(self):
        return self.keys()

    def toJSON(self):
        print("toJSON of ParameterDict called!")
        return self.__dict__


if __name__ == '__main__':
    test_parameter = Parameter()
    print(test_parameter.default)
    test_parameter_int = Parameter(parameterType=int)
    print(test_parameter_int.default)
    print(test_parameter.value)
    test_parameter_nonexistent = Parameter(parameterType=object)