from enum import Enum

import matplotlib
import numpy as np
import wx
from matplotlib.backends.backend_wx import NavigationToolbar2Wx as NavigationToolbar2Wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable

import layers
from ui.LayerListCtrl import LayerListCtrl
from ui.ValueChoice import ValueChoice
from layers.Layer import Layer
from layers.rasterLayers.RasterLayer import RasterLayer


class MainCanvasPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.figure = Figure()

        self.axes = self.figure.add_subplot(111)
        divider = make_axes_locatable(self.axes)
        self.colorbar_axes = divider.append_axes("right", size="5%", pad=0.05)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        self.toolbar.Realize()

        plt_sizer = wx.BoxSizer(wx.VERTICAL)
        plt_sizer.Add(self.canvas, 1, wx.EXPAND)
        plt_sizer.Add(self.toolbar, 0, wx.EXPAND)

        self.ctrl_sizer = wx.WrapSizer()

        layer_sizer = wx.BoxSizer(wx.VERTICAL)
        self.layer_list = LayerListCtrl(self, style=wx.LC_REPORT)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.display_current_layer)
        self.layer_list.Bind(LayerListCtrl.EVT_LIST_UPDATE, self.render_noise)

        layer_button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        layer_add_choice = wx.Choice(self, choices=["Add...", *layers.layer_names.keys()])
        layer_add_choice.Select(0)
        layer_rem_button = wx.Button(self, -1, label="Remove")
        layer_button_sizer.Add(layer_add_choice)
        layer_button_sizer.AddStretchSpacer()
        layer_button_sizer.Add(layer_rem_button)
        layer_sizer.Add(self.layer_list, 1, wx.EXPAND)
        layer_sizer.Add(layer_button_sizer)
        layer_sizer.Add(self.ctrl_sizer)

        layer_add_choice.Bind(wx.EVT_CHOICE, self.layer_list.new_layer)
        layer_rem_button.Bind(wx.EVT_BUTTON, self.layer_list.rem_current_layer)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(plt_sizer, 1, wx.EXPAND)
        main_sizer.Add(layer_sizer, 1, wx.EXPAND)

        self.SetSizer(main_sizer)

    def render_noise(self, event):
        self.update_ctrls()
        self.axes.clear()
        pic = np.zeros((1, 1))
        maxres = 1

        for layer in self.layer_list.get_enabled_layers():
            layer.calculate()
            if issubclass(type(layer), RasterLayer):
                pixels = layer.pixels

                if layer.xshift > 0 or layer.yshift > 0:
                    pixels = np.roll(pixels, (layer.yshift,layer.xshift), (0,1))
                    pixels[:,0:layer.xshift] = 0
                    pixels[0:layer.yshift,:] = 0

                pic = pixels + pic

            if hasattr(layer, "draw"):
                layer.draw(self.axes)

            if layer.res > maxres:
                maxres = layer.res

        if pic is not np.zeros((1, 1)):
            cmap = matplotlib.colormaps['viridis']
            cmap.set_under('white')
            cmap.set_over('white')

            im = self.axes.imshow(pic, cmap=cmap)
            self.figure.colorbar(im, cax=self.colorbar_axes)

        self.axes.set_xlim(0, maxres - 1)
        self.axes.set_ylim(0, maxres - 1)
        self.canvas.draw()

    def display_current_layer(self, event):
        layer = self.layer_list.get_current_layer()
        self.ctrl_sizer.Clear(True)
        if layer is not None:
            for parameter in layer.parameters.values():
                sizer = wx.BoxSizer(wx.HORIZONTAL)

                input = None

                if issubclass(parameter.parameterType, Enum):
                    input = ValueChoice(self, list(parameter.parameterType))
                    input.SetValue(parameter.value)
                elif hasattr(parameter, "value_choices"):
                    input = ValueChoice(self, parameter["value_choices"])
                    input.SetValue(parameter.value)
                elif parameter.parameterType in [int]:
                    input = wx.Slider(self, id=-1, value=parameter.value, minValue=parameter.min,
                                      maxValue=parameter.max,
                                      style=wx.SL_AUTOTICKS | wx.SL_VALUE_LABEL)
                elif parameter.parameterType is str:
                    input = wx.TextCtrl(self, -1, value=parameter.value)
                elif parameter.parameterType is bool:
                    input = wx.CheckBox(self, id=-1, label=parameter.name)
                    input.SetValue(parameter.value)
                elif parameter.parameterType is Layer:
                    input = ValueChoice(self, self.layer_list.layer_list)
                    input.SetValue(parameter.value)

                if input is not None:
                    input.parameter = parameter
                    input.SetToolTip(parameter.desc)
                    input.Bind(wx.EVT_SLIDER, self.layer_list.update_current_layer_from_event)
                    input.Bind(wx.EVT_TEXT, self.layer_list.update_current_layer_from_event)
                    input.Bind(wx.EVT_CHECKBOX, self.layer_list.update_current_layer_from_event)
                    input.Bind(wx.EVT_CHOICE, self.layer_list.update_current_layer_from_event)

                    if parameter.parameterType is not bool:
                        label = wx.StaticText(self, label=parameter.name)
                        sizer.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL)
                        sizer.AddSpacer(10)

                    sizer.Add(input, 1, wx.EXPAND)
                    self.ctrl_sizer.Add(sizer)
        self.Layout()

    def update_ctrls(self):
        for child in MainCanvasPanel.get_all_children(self.ctrl_sizer):
            if child.GetWindow() is not None and "parameter" in child.GetWindow().__dict__:
                window = child.GetWindow()
                parameter = window.parameter
                if parameter.value != window.GetValue():
                    window.SetValue(parameter.value)
                if isinstance(window, wx.Slider):
                    window.SetMin(parameter.min)
                    window.SetMax(parameter.max)

    def get_all_children(sizer):
        children = list()
        for child in sizer.GetChildren():
            children.append(child)
            if child.GetSizer() is not None:
                children.extend(MainCanvasPanel.get_all_children(child.GetSizer()))

        return children

    def GetLayerList(self):
        return self.layer_list