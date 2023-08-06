import os

import jsonpickle, wx

import exporters, importers
from layers import ImportedRasterLayer
from ui.MainCanvasPanel import MainCanvasPanel


class MainFrame(wx.Frame):
    def __init__(self, title):
        super().__init__(parent=None, id=-1, title=title)
        self.panel = MainCanvasPanel(self)

        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        export_menu = wx.Menu()
        import_menu = wx.Menu()

        export_item = wx.MenuItem(file_menu, wx.ID_CONVERT, "", "Export data for conservation planning software", wx.ITEM_NORMAL, export_menu)
        import_item = wx.MenuItem(file_menu, -1, "Import", "Import existing data", wx.ITEM_NORMAL, import_menu)
        save_item = wx.MenuItem(file_menu, wx.ID_SAVE, "", "Save current project", wx.ITEM_NORMAL, None)
        open_item = wx.MenuItem(file_menu, wx.ID_OPEN, "", "Open the current project", wx.ITEM_NORMAL, None)

        file_menu.Bind(wx.EVT_MENU, self.save_project, save_item)
        file_menu.Bind(wx.EVT_MENU, self.open_project, open_item)

        for exporter_name, exporter_class in exporters.exporter_names.items():
            exporter_item = wx.MenuItem(export_menu, wx.ID_CONVERT, exporter_name, f"Export data for {exporter_name}", wx.ITEM_NORMAL, None)
            export_menu.Append(exporter_item)
            export_menu.Bind(wx.EVT_MENU, exporter_class, exporter_item)

        for importer_name, importer_class in importers.importer_names.items():
            print(importer_name, ":", importer_class)
            importer_item = wx.MenuItem(import_menu, -1, importer_name, f"Import data from {importer_name}", wx.ITEM_NORMAL, None)
            import_menu.Append(importer_item)
            import_menu.Bind(wx.EVT_MENU, importer_class, importer_item)

        menubar.Append(file_menu, "&File")
        file_menu.Append(save_item)
        file_menu.Append(open_item)
        file_menu.Append(export_item)
        file_menu.Append(import_item)

        self.SetMenuBar(menubar)
        self.panel.Show()

    def GetPanel(self) -> MainCanvasPanel:
        return self.panel

    def save_project(self, event):
        file_dialog = wx.FileDialog(parent=event.GetEventObject().GetWindow(), message="",
                                    defaultDir="/home/lukas/Downloads", defaultFile="project.json",
                                    wildcard="JSON files (.json)", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if file_dialog.ShowModal() == wx.ID_OK:
            self.update_rel_paths(file_dialog.GetPath())

            with open(file_dialog.GetPath(), "w") as project_file:
                project_file.write(
                    jsonpickle.encode(self.GetPanel().GetLayerList().layer_list, warn=True, indent=4, keys=True))

    def open_project(self, event):
        file_dialog = wx.FileDialog(parent=event.GetEventObject().GetWindow(), message="",
                                    defaultDir="/home/lukas/Downloads", defaultFile="project.json",
                                    wildcard="JSON files (.json)", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if file_dialog.ShowModal() == wx.ID_OK:
            os.chdir(os.path.dirname(file_dialog.GetPath()))

            with open(file_dialog.GetPath(), "r") as project_file:
                layer_list = jsonpickle.decode(project_file.read())
                self.GetPanel().GetLayerList().set_layer_list(layer_list)

    def update_rel_paths(self, dest_path):
        os.chdir(os.path.dirname(dest_path))
        for layer in self.GetPanel().GetLayerList().layer_list:
            if isinstance(layer, ImportedRasterLayer):
                layer.update_rel_path()