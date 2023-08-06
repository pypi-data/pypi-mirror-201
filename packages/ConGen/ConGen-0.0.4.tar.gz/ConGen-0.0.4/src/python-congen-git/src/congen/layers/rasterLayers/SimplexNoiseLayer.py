import noise_randomized

from layers.rasterLayers.NoiseRasterLayer import NoiseRasterLayer


class SimplexNoiseLayer(NoiseRasterLayer):
    def __init__(self, noise_function=noise_randomized.snoise2, **kwargs):
        super().__init__(noise_function=noise_function, type="Simplex", **kwargs)
