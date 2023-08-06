import numpy as np

from layers.LayerUsage import LayerUsage
from layers.Parameter import ParameterDict, Parameter


class Layer:
    def __init__(self, enabled=True, **kwargs):
        if not hasattr(self, "parameters"):
            self.parameters = ParameterDict()
        if not hasattr(self, "dependentLayers"):
            self.dependentLayers = list()

        self.parameters.extend([
            Parameter(name="name", desc="Name of the Layer", parameterType=str, default="New Layer"),
            Parameter(name="seed", desc="Random seed for the layer",
                      parameterType=int, min=0, max=100, default=0, invalidates_cache=True),
            Parameter(name="weight", desc="Weight of the layer", parameterType=int, min=1, max=10, default=5,
                      invalidates_cache=True),
            Parameter(name="res", desc="Resolution of the layer in pixels (affects width and height)",
                      parameterType=int, min=10, max=200, default=100, invalidates_cache=True),
            Parameter(name="xshift", desc="Amount to shift this layer left / right",
                      parameterType=int, min=0, max=100, default=0),
            Parameter(name="yshift", desc="Amount to shift this layer top / down",
                      parameterType=int, min=0, max=100, default=0),
            Parameter(name="layer_usage", desc="Usage of this layer in exported files",
                      parameterType=LayerUsage, min=None, max=None, default=None)
        ])
        self.update(enabled=enabled, **kwargs)
        self.clear_cache()

    def clear_cache(self):
        self.points = None
        self.pixels = None
        self.graph = None
        self.generator = None
        self.importer = None
        for layer in self.dependentLayers:
            layer.clear_cache()

    def update(self, **kwargs):
        if any(item in kwargs for item in self.parameters.cache_invalidators):
            self.clear_cache()

        if "layer_usage" in list(kwargs.keys()):
            if kwargs["layer_usage"] == LayerUsage.LAYER_USAGE_FEATURE:
                self.parameters.extend([
                    Parameter(name="target", desc="Minimum amount of the feature to be in the solution",
                              parameterType=int, min=0, max=100, default=0),
                    Parameter(name="prop", desc="Minimum proportion of the feature to be in the solution",
                              parameterType=int, min=0, max=100, default=0)
                ])

        for key in list(kwargs.keys()):
            if key in self.parameters:
                self.parameters[key].value = kwargs.pop(key)

        self.__dict__.update(kwargs)

        self.parameters["xshift"].max = self.res
        self.parameters["yshift"].max = self.res

    # only gets called for parameters that are not found otherwise
    def __getattr__(self, item):
        try:
            return self.parameters[item].value
        except Exception:
            raise AttributeError(f"{self.__class__.__name__} has no attribute {item}.")
        

    def get_generator(self):
        if not hasattr(self, "generator") or self.generator is None:
            self.generator = np.random.default_rng(self.seed)
        return self.generator

    def __str__(self):
        return self.name

    def toJSON(self):
        print("toJSON of Layer called!")
        print(self.parameters)
        return self.parameters

    def __getstate__(self):
        self.clear_cache()
        dict = self.__dict__.copy()
        dict["dependentLayers"] = []
        return dict

    def __setstate__(self, state):
        print(f"De-pickling layer {state['parameters']['name']['value']}")
        self.__dict__.update(state)
        if hasattr(self, "dependingLayer") and self.dependingLayer is not None:
            self.dependingLayer.dependentLayers.append(self)