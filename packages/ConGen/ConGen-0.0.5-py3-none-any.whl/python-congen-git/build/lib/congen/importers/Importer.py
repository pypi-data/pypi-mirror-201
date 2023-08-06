import os

import wx

from importers.ImporterType import ImporterType


class Importer(metaclass=ImporterType):
    def __init__(self, event: wx.CommandEvent = None, wildcard="*.*", layer = None):
        self.event = event
        self.layer = layer

        if self.layer is None:
            self.layer_list = self.event.GetEventObject().GetWindow().GetPanel().GetLayerList()
            file_dialog = wx.FileDialog(parent=event.GetEventObject().GetWindow(), message="",
                                        defaultDir="/home/lukas/Downloads", defaultFile="project.json",
                                        wildcard=wildcard, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)

            if file_dialog.ShowModal() == wx.ID_OK:
                from layers.rasterLayers.ImportedRasterLayer import ImportedRasterLayer
                self.paths = file_dialog.GetPaths()

                for path in self.paths:
                    layer = ImportedRasterLayer(importer_type = self.__class__.__name__,
                                                name=os.path.basename(path),
                                                abs_file_path=os.path.abspath(path),
                                                rel_file_path=os.path.relpath(path))
                    self.layer_list.add_layer(layer)

    def import_file(self):
        pass
