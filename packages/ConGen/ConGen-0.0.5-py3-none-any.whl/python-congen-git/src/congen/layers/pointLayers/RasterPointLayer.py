from layers.Parameter import Parameter
from layers.DependentLayer import DependentLayer
from layers.pointLayers.PointLayer import PointLayer
import numpy as np


class RasterPointLayer(PointLayer, DependentLayer):
    def __init__(self, **kwargs):
        super().__init__()
        self.parameters.append(Parameter(name="lowerThreshold", desc="Place points in cells with at least this value",
                                         parameterType=int, min=-100, max=100, default=-100, invalidates_cache=True))
        self.parameters.append(Parameter(name="upperThreshold", desc="Place points in cells with at most this value",
                                         parameterType=int, min=-100, max=100, default=100, invalidates_cache=True))
        self.parameters.append(Parameter(name="cellFillProbability", desc="Percentage of cells to fill with points",
                                         parameterType=int, min=0, max=100, default=100, invalidates_cache=True))
        self.update(**kwargs)

    def calculate(self):
        if self.points is None and self.dependingLayer is not None and self.dependingLayer.pixels is not None:
            self.get_generator()
            self.pixels = self.dependingLayer.pixels
            matching = (self.pixels >= self.lowerThreshold) * (self.pixels <= self.upperThreshold)
            matching = matching * self.cellFillProbability >= self.generator.uniform(
                self.parameters["cellFillProbability"].min, self.parameters["cellFillProbability"].max, matching.shape)
            self.points = np.array(matching.T.nonzero())
