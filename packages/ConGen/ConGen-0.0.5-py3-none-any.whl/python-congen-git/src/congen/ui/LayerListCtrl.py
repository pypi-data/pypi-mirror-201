import wx
from wx.lib import newevent

import layers
from collections import defaultdict

from layers.Parameter import ParameterDict


class LayerListCtrl(wx.ListCtrl):
    EventListUpdate, EVT_LIST_UPDATE = newevent.NewEvent()
    current_instance = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.EnableCheckBoxes()
        self.layer_list = []
        self.Bind(wx.EVT_LIST_ITEM_CHECKED, self.update_checked)
        self.Bind(wx.EVT_LIST_ITEM_UNCHECKED, self.update_checked)
        LayerListCtrl.current_instance = self

    def set_layer_list(self, layer_list):
        self.layer_list = layer_list
        self.refresh_list()

    def new_layer(self, event):
        layer = congen.layers.layer_names[event.String]()
        layer.update(name=f'{event.String} Layer {len(self.layer_list)}')
        self.add_layer(layer)

    def add_layer(self, layer):
        self.layer_list.append(layer)
        self.refresh_list()

    def rem_current_layer(self, event):
        if self.GetSelectedItemCount():
            index = self.GetFirstSelected()
            self.layer_list.remove(self.layer_list[index])

            self.refresh_list()

    def get_all_columns(self):
        columns = list()
        for i in range(self.GetColumnCount()):
            columns.append(self.GetColumn(i))

        return columns

    def get_all_layers(self):
        return self.layer_list

    def get_all_column_names(self):
        column_names = list()
        for column in self.get_all_columns():
            column_names.append(column.Text)

        return column_names

    def get_all_parameters(self):
        parameters = ParameterDict()
        for layer in self.layer_list:
            parameters.extend(layer.parameters.values())

        return parameters

    def refresh_columns(self):
        column_names = self.get_all_column_names()
        for parameter_id in self.get_all_parameters().get_ids():
            if parameter_id not in column_names:
                self.AppendColumn(parameter_id)

    def refresh_layer(self, layer_index):
        layer = self.layer_list[layer_index]
        layer_params = defaultdict(lambda: "N/A")
        layer_params.update(layer.__dict__)
        layer_params.update({parameter.name: parameter.value for parameter in layer.parameters.values()})
        self.CheckItem(layer_index, layer.enabled)
        for column_index, column in enumerate(self.get_all_columns()):
            self.SetItem(layer_index, column_index, str(layer_params[column.Text]))

    def refresh_list(self):
        self.refresh_columns()

        previous_index = -1
        if self.GetSelectedItemCount():
            previous_index = self.GetFirstSelected()

        self.DeleteAllItems()
        for index, layer in enumerate(self.layer_list):
            self.InsertItem(index, str(index))
            self.refresh_layer(index)

        if previous_index >= 0 and self.ItemCount > 0:
            self.Select(previous_index)

        wx.PostEvent(self, LayerListCtrl.EventListUpdate())

    def update_checked(self, event):
        self.layer_list[event.Index].update(enabled=self.IsItemChecked(event.Index))
        wx.PostEvent(self, LayerListCtrl.EventListUpdate())

    def update_current_layer(self, **kwargs):
        if self.GetSelectedItemCount():
            index = self.GetFirstSelected()
            self.layer_list[index].update(**kwargs)

            self.refresh_layer(index)

            wx.PostEvent(self, LayerListCtrl.EventListUpdate())

    def update_current_layer_from_event(self, event):
        self.update_current_layer(**{event.EventObject.parameter.name: event.EventObject.GetValue()})

    def get_current_layer(self):
        if self.GetSelectedItemCount():
            index = self.GetFirstSelected()
            return self.layer_list[index]

    def get_enabled_layers(self):
        return filter(lambda i: i.enabled, self.layer_list)

    def toJSON(self):
        return {"layer_list": self.layer_list}
