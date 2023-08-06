import noise_randomized
import numpy as np

from layers.Parameter import Parameter
from layers.rasterLayers.RasterLayer import RasterLayer


class NoiseRasterLayer(RasterLayer):
    def __init__(self, **kwargs):
        super().__init__()
        self.parameters.append(Parameter(name="frequency", desc="Frequency of the perlin noise layer",
                                         parameterType=int, min=1, max=100, default=1, invalidates_cache=True))
        self.parameters.append(Parameter(name="octaves", desc="Octaves of the perlin noise layer",
                                         parameterType=int, min=1, max=20, default=10, invalidates_cache=True))
        self.parameters.append(Parameter(name="persistence", desc="Persistence of the perlin noise layer",
                                         parameterType=int, min=1, max=10, default=5, invalidates_cache=True))
        self.parameters.append(Parameter(name="lacunarity", desc="Lacunarity of the perlin noise layer",
                                         parameterType=int, min=1, max=10, default=2, invalidates_cache=True))
        self.update(**kwargs)

    def calculate(self):
        if self.pixels is None:
            print(f'Recalculating layer {self.name}')
            noise_randomized.randomize(256, int(self.seed))

            self.pixels = np.array([[self.noise_function(i / (self.frequency * self.res), j / (self.frequency * self.res),
                                                      octaves=self.octaves, persistence=self.persistence,
                                                      lacunarity=self.lacunarity)
            for j in range(self.res)] for i in range(self.res)])

        super().calculate()


