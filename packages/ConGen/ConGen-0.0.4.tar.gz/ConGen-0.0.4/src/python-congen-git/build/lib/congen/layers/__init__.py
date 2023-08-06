from layers.rasterLayers import SimplexNoiseLayer
from layers.graphLayers.FullGraphLayer import FullGraphLayer
from layers.graphLayers.GraphLayer import GraphLayer
from layers.pointLayers.clustered.KMeansClusteredPointLayer import KMeansClusteredPointLayer
from layers.graphLayers.RandomGraphLayer import RandomGraphLayer
import layers.rasterLayers.SimplexNoiseLayer
from layers.rasterLayers.PerlinNoiseLayer import PerlinNoiseLayer
from layers.rasterLayers.PointRasterLayer import PointRasterLayer
from layers.pointLayers.RasterPointLayer import RasterPointLayer
from layers.pointLayers.SimpleRandomPointLayer import SimpleRandomPointLayer
from layers.pointLayers.StratifiedRandomPointLayer import StratifiedRandomPointLayer
from layers.rasterLayers.ImportedRasterLayer import ImportedRasterLayer


def create_multilayer_class(*superclasses):
    class MultilayerClass(*superclasses):
        def __init__(self, **kwargs):
            for superclass in superclasses:
                superclass.__init__(self, **kwargs)
        def calculate(self):
            self.generator = None
            for superclass in superclasses:
                superclass.calculate(self)

        def draw(self, axes):
            for superclass in superclasses:
                if hasattr(superclass, "draw"):
                    superclass.draw(self, axes)

    return MultilayerClass


layer_names = {
    "Perlin": PerlinNoiseLayer,
    "Simplex": SimplexNoiseLayer,
    "SimpleRandomPointLayer": SimpleRandomPointLayer,
    "StratifiedRandomPointLayer": StratifiedRandomPointLayer,
    "RasterPointLayer": RasterPointLayer,
    "KMeansClusteredPointLayer": KMeansClusteredPointLayer,
    "FullGraphLayer": FullGraphLayer,
    "RandomGraphLayer": RandomGraphLayer,
    "ImportedRasterLayer": ImportedRasterLayer,
}
