import wx

from layers import GraphLayer
from layers.LayerUsage import LayerUsage
from layers.rasterLayers.RasterLayer import RasterLayer


class Exporter:
    def __init__(self, event: wx.CommandEvent):
        self.event = event
        self.get_layers()

        dir_dialog = wx.DirDialog(event.GetEventObject().GetWindow(), "Choose export directory", "/home/lukas/Downloads", wx.DD_DEFAULT_STYLE)
        if dir_dialog.ShowModal() == wx.ID_OK:
            self.dest_path = dir_dialog.GetPath()
            self.export()
        else:
            self.dest_path = None

    def get_layers(self):
        self.layer_list = self.event.GetEventObject().GetWindow().GetPanel().GetLayerList().get_all_layers()
        self.cost_layers = list(filter(lambda layer: layer.layer_usage == LayerUsage.LAYER_USAGE_COST, self.layer_list))
        self.feature_layers = list(filter(lambda layer: layer.layer_usage == LayerUsage.LAYER_USAGE_FEATURE, self.layer_list))
        self.graph_layers = list(filter(lambda layer: isinstance(layer, GraphLayer), self.layer_list))
        self.raster_layers = list(filter(lambda layer: isinstance(layer, RasterLayer), self.layer_list))

    def export(self):
        pass
