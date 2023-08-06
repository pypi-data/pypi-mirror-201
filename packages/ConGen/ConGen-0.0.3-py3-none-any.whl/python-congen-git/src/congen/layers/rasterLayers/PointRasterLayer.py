import numpy as np
from matplotlib.patches import FancyBboxPatch, BoxStyle

from layers.Parameter import Parameter
from layers.rasterLayers.RasterLayer import RasterLayer


class PointRasterLayer(RasterLayer):
    def __init__(self, **kwargs):
        super().__init__()
        self.parameters.append(Parameter(name="fullradius", desc="corner radius for the full box",
                                         parameterType=int, min=1, max=100, default=1, invalidates_cache=True))
        self.parameters.append(Parameter(name="zeroradius", desc="corner radius for the zero box",
                                         parameterType=int, min=1, max=100, default=1, invalidates_cache=True))
        self.update(**kwargs)

    def calculate_circular_mask(w, h, center, radius, maxradius):
        Y, X = np.ogrid[:h, :w]
        # Everything that is closer to the center than the radius of the center will be 0 away from center
        dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2) - radius
        dist_from_center = np.maximum(dist_from_center, 0)

        dist_between_radiae = max(maxradius - radius, 1)

        dist_from_maxradius = dist_between_radiae - dist_from_center
        dist_from_maxradius = np.maximum(dist_from_maxradius, 0)

        mask = dist_from_maxradius / np.maximum(np.max(dist_from_maxradius), 1)

        return mask

    def draw_radius(axes, point, radius, color):
        patch = FancyBboxPatch((point[0], point[1]), width=0, height=0,
                               facecolor='none', edgecolor=color, boxstyle=BoxStyle("Round", pad=radius))
        axes.add_patch(patch)

    def calculate(self):
        if self.pixels is None:
            self.pixels = np.zeros((self.res, self.res))
            for point in self.points.T:
                self.pixels += PointRasterLayer.calculate_circular_mask(self.res, self.res, center=point, radius=self.fullradius, maxradius=self.zeroradius)

        super().calculate()

    def draw(self, axes):
        for point in self.points.T:
            PointRasterLayer.draw_radius(axes, point, self.zeroradius, 'blue')
            PointRasterLayer.draw_radius(axes, point, self.fullradius, 'red')
