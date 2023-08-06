from layers.Parameter import Parameter
from layers.DependentLayer import DependentLayer
from layers.pointLayers.PointLayer import PointLayer
from sklearn.cluster import KMeans


class KMeansClusteredPointLayer(PointLayer, DependentLayer):
    def __init__(self, **kwargs):
        super().__init__()
        self.parameters.extend([
            Parameter(name="num_clusters", desc="Number of clusters", parameterType=int, min=1, max=100, default=5)
        ])
        super().update(**kwargs)

    def calculate(self):
        super().calculate()
        kmeans = KMeans(n_clusters=self.num_clusters, random_state=0, n_init="auto").fit(self.dependingLayer.points.T)
        self.points = kmeans.cluster_centers_.T