from layers.graphLayers.GraphLayer import GraphLayer
import igraph as ig


class FullGraphLayer(GraphLayer):
    def calculate(self):
        if self.graph is None:
            self.graph = ig.Graph.Full(n=len(self.dependingLayer.points.T))