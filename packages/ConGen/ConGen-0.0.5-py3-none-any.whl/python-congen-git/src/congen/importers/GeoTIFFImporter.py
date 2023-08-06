import os

import numpy as np
import wx
from osgeo import gdal

from importers.Importer import Importer


class GeoTIFFImporter(Importer):
    def __init__(self, event: wx.CommandEvent = None, wildcard="*.tif", layer=None):
        super().__init__(event, wildcard=wildcard, layer=layer)

    def import_file(self):
        layer = self.layer
        try:
            gdal_data = gdal.Open(layer.abs_file_path, gdal.GA_ReadOnly)
            layer.rel_file_path = os.path.relpath(layer.abs_file_path)
        except Exception:
            try:
                gdal_data = gdal.Open(layer.rel_file_path, gdal.GA_ReadOnly)
                layer.abs_file_path = os.path.abspath(layer.rel_file_path)
            except Exception:
                raise FileNotFoundError(f"File could not be found under absolute path {layer.abs_file_path} or "
                                        f"relative path {layer.rel_file_path}")
        raster_band = gdal_data.GetRasterBand(1)
        img_array : np.ndarray = raster_band.ReadAsArray().astype(np.double)
        print(np.sum(img_array != 65535))
        print("Driver: {}/{}".format(gdal_data.GetDriver().ShortName, gdal_data.GetDriver().LongName))
        print("Size is {} x {} x {}".format(gdal_data.RasterXSize, gdal_data.RasterYSize, gdal_data.RasterCount))
        print(f"Zero value is {raster_band.GetNoDataValue()}")
        geotransform = gdal_data.GetGeoTransform()
        if geotransform:
            print("Origin = ({}, {})".format(geotransform[0], geotransform[3]))
            print("Pixel Size = ({}, {})".format(geotransform[1], geotransform[5]))

        print("Band Type={}".format(gdal.GetDataTypeName(raster_band.DataType)))

        min = raster_band.GetMinimum()
        max = raster_band.GetMaximum()
        if not min or not max:
            (min, max) = raster_band.ComputeRasterMinMax(True)
        print("Min={:.3f}, Max={:.3f}".format(min, max))
        img_array[img_array == raster_band.GetNoDataValue()] = np.nan

        if raster_band.GetOverviewCount() > 0:
            print("Band has {} overviews".format(raster_band.GetOverviewCount()))

        if raster_band.GetRasterColorTable():
            print("Band has a color table with {} entries".format(raster_band.GetRasterColorTable().GetCount()))

        scanline = raster_band.ReadAsArray(0, 0, raster_band.XSize, raster_band.YSize).astype(np.float64)
        print(scanline)
        print(gdal_data.RasterCount)

        layer.update(
            res=np.maximum(gdal_data.RasterXSize, gdal_data.RasterYSize),
            min_cutoff=min,
            max_cutoff=max,
            min_value=int(min), #TODO: This might cause values to be altered during rescaling, add support for float
            max_value=int(max),
            weight=1
        )
        layer.pixels = img_array
