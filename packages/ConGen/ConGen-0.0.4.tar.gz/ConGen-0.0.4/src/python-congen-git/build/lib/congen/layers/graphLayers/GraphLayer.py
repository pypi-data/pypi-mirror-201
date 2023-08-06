from layers.DependentLayer import DependentLayer
import igraph as ig


class GraphLayer(DependentLayer):
    def draw(self, axes):
        self.calculate()
        ig.plot(self.graph, target=axes, layout = self.dependingLayer.points.T)