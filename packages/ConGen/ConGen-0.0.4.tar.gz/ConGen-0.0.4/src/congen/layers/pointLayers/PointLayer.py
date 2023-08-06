from matplotlib import colors as mcolors

from layers.LayerType import LayerType
from layers.Layer import Layer


class PointLayer(Layer):
    colors = list(mcolors.TABLEAU_COLORS.values())
    def __init__(self, points = None, layerType = LayerType.LAYER_TYPE_POINTS, color = None, **kwargs):
        if color is None:
            color = self.colors.pop(0)
        super().__init__(points = points, layerType = layerType, color = color, **kwargs)

    def draw(self, axes):
        self.calculate()
        if self.points is not None:
            axes.scatter(self.points[0], self.points[1], c=self.color)

    def calculate(self):
        pass