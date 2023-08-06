import numpy as np

from layers.LayerType import LayerType
from layers.Parameter import Parameter
from layers.Layer import Layer


class RasterLayer(Layer):
    def __init__(self, pixels = None, layerType = LayerType.LAYER_TYPE_RASTER, **kwargs):
        super().__init__()
        self.parameters.extend([
            Parameter(name="min_value", desc="Minimum value of each pixel",
                      parameterType=int, min=-100, max=100, default=0),
            Parameter(name="max_value", desc="Maximum value of each pixel",
                      parameterType=int, min=-100, max=100, default=100),
        ])
        super().update(pixels = pixels, layerType = layerType, **kwargs)

    def calculate(self):
        min_value = np.nanmin(self.pixels)
        max_value = np.nanmax(self.pixels)
        scale = (self.max_value - self.min_value) / (max_value - min_value)
        offset = self.min_value - min_value * scale
        self.pixels = self.weight * (self.pixels * scale + offset)
