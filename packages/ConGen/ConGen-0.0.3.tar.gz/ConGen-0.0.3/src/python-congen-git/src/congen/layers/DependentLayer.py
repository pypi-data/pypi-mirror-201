from layers.Parameter import Parameter
from layers.Layer import Layer


class DependentLayer(Layer):
    def __init__(self, **kwargs):
        super().__init__()
        self.parameters.append(Parameter(name="dependingLayer", desc="Layer this layer depends on",
                                         parameterType=Layer, min=None, max=None, default=None, invalidates_cache=True))
        self.update(**kwargs)

    def update(self, **kwargs):
        super().update(**kwargs)
        if "dependingLayer" in kwargs.keys() and kwargs["dependingLayer"] is not None:
            kwargs["dependingLayer"].dependentLayers.append(self)

    def calculate(self):
        pass