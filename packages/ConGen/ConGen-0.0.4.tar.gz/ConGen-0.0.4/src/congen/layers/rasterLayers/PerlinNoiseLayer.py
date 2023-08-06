import noise_randomized

from layers.rasterLayers.NoiseRasterLayer import NoiseRasterLayer


class PerlinNoiseLayer(NoiseRasterLayer):
    def __init__(self, noise_function=noise_randomized.pnoise2, **kwargs):
        super().__init__(noise_function=noise_function, type="Perlin", **kwargs)
