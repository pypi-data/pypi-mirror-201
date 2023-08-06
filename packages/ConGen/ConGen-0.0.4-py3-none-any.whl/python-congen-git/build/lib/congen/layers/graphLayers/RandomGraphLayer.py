from layers.graphLayers.FullGraphLayer import FullGraphLayer
from layers.Parameter import Parameter


class RandomGraphLayer(FullGraphLayer):
    def __init__(self, **kwargs):
        super().__init__()
        self.parameters.extend([
            Parameter(name="edge_count", desc="Number of edges that are randomly drawn from the full graph",
                      parameterType=int, min=0, max=100, default=100, invalidates_cache=True)
        ])
        self.update(**kwargs)
    def calculate(self):
        if self.graph is None:
            super().calculate()
            self.parameters["edge_count"].max = self.graph.ecount()
            edgelist = self.get_generator().permutation(len(self.graph.get_edgelist()))[:self.edge_count]
            self.graph = self.graph.subgraph_edges(edgelist, delete_vertices=False)