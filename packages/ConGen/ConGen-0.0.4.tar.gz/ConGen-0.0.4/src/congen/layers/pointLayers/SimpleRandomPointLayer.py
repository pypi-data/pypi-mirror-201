from layers.Parameter import Parameter
from layers.pointLayers.PointLayer import PointLayer


class SimpleRandomPointLayer(PointLayer):
    def __init__(self, type = "Simple Random Points", **kwargs):
        super().__init__()
        self.parameters.append(Parameter(name = "nPoints", desc = "Number of points",
                                         parameterType=int, min=1, max=200, default=25, invalidates_cache=True))
        self.update(type = type, **kwargs)

    def calculate(self):
        if self.points is None:
            self.get_generator()
            self.points = self.generator.uniform(0, self.res, (2, self.nPoints))
        return self.points
