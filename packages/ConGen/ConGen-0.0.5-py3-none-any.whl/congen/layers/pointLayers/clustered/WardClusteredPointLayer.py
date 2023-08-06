from layers.Parameter import Parameter
from layers.DependentLayer import DependentLayer
from layers.pointLayers.PointLayer import PointLayer
from sklearn.cluster import AgglomerativeClustering
import numpy as np



"""
TODO: Fix this class
"""
class WardClusteredPointLayer(PointLayer, DependentLayer):
    def __init__(self, **kwargs):
        super().__init__()
        self.parameters.extend([
            Parameter(name="num_clusters", desc="Number of clusters", parameterType=int, min=0, max=100, default=0),
            Parameter(name="max_distance", desc="Maximum cluster size", parameterType=int, min=0, max=100, default=0)
        ])
        super().update(**kwargs)

    def update(self, **kwargs):
        keys = list(kwargs.keys())
        if "num_clusters" in keys:
            self.max_distance = 0
        if "max_distance" in kwargs:
            self.num_clusters = 0
        super().update(**kwargs)

    def calculate(self):
        super().calculate()
        num_clusters = None if self.num_clusters == 0 else self.num_clusters
        max_distance = None if self.max_distance == 0 else self.max_distance
        input_points = self.dependingLayer.points.T

        print(input_points.shape)

        ward = AgglomerativeClustering(n_clusters = num_clusters, distance_threshold=max_distance).fit(input_points)

        print(ward.labels_)

        points = []
        for cluster_id in range(ward.n_clusters_):
            points.append(input_points[ward.labels_ == cluster_id].mean(axis=0))
        print(points)
        self.points = np.array(points).T