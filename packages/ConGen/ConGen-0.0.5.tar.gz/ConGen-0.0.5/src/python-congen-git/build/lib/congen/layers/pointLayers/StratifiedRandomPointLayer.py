import numpy as np

from layers.Parameter import Parameter
from layers.pointLayers.PointLayer import PointLayer


class StratifiedRandomPointLayer(PointLayer):
    def __init__(self, type="Stratified Random Points", **kwargs):
        super().__init__()
        self.parameters.append(Parameter(name="xCells", desc="Number of horizontal cells",
                                         parameterType=int, min=1, max=50, default=10, invalidates_cache=True))
        self.parameters.append(Parameter(name="yCells", desc="Number of vertical cells",
                                         parameterType=int, min=1, max=50, default=10, invalidates_cache=True))
        self.parameters.append(Parameter(name="pointsPerCell", desc="Number of points per cell",
                                         parameterType=int, min=1, max=10, default=1, invalidates_cache=True))
        self.parameters.append(Parameter(name="displayCells", desc="Display line borders for cells",
                                         parameterType=bool, default=True))
        self.parameters.append(Parameter(name="cellFillProbability", desc="Percentage of cells to fill with points",
                                         parameterType=int, min=0, max=100, default=100, invalidates_cache=True))
        self.parameters.append(Parameter(name="nPoints", desc="Total number of points to display",
                                         parameterType=int, min=0, max=100,
                                         default=100, invalidates_cache=True))
        self.update(type=type, **kwargs)

    def update(self, **kwargs):
        super().update(**kwargs)
        self.update_max_point_num()

    def calculate(self):
        if self.points is None:

            self.xLines = np.linspace(0, self.res, self.xCells+1, dtype=int)
            self.yLines = np.linspace(0, self.res, self.yCells+1, dtype=int)
            self.get_generator()

            self.points = list()

            for x in range(self.xCells):
                for y in range(self.yCells):
                        for n in range(self.pointsPerCell):
                            # Always generate point, even if it is not added, so generator state does not change depending
                            # on cellFillProbability
                            point = [self.generator.uniform(self.xLines[x], self.xLines[x+1]),
                                     self.generator.uniform(self.yLines[y], self.yLines[y+1])]
                            if self.generator.uniform(0, 100) >= 100 - self.cellFillProbability:
                                self.points.append(point)

            self.points = np.array(self.points)
            self.generator.shuffle(self.points)
            if self.nPoints < len(self.points):
                self.points = self.points[:self.nPoints]
            self.points = self.points.T

        return self.points

    def draw(self, axes):
        super().draw(axes)
        if self.displayCells:
            axes.hlines(self.yLines, 0, self.res, colors=self.color)
            axes.vlines(self.xLines, 0, self.res, colors=self.color)

    def update_max_point_num(self):
        if hasattr(self, "xCells") and hasattr(self, "yCells") and hasattr(self, "pointsPerCell"):
            self.parameters["nPoints"].max = self.xCells * self.yCells * self.pointsPerCell
