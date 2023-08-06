import os, re, unicodedata

import numpy as np

from exporters.Exporter import Exporter
from osgeo import gdal, gdal_array


class GeoTIFFExporter(Exporter):
    def export(self):
        self.export_raster_layers()

    def export_raster_layers(self, no_data_value=65535):
        """
        Useful links:
        https://here.isnew.info/how-to-save-a-numpy-array-as-a-geotiff-file-using-gdal.html
        https://borealperspectives.org/2014/01/16/data-type-mapping-when-using-pythongdal-to-write-numpy-arrays-to-geotiff/
        https://gis.stackexchange.com/questions/164853/reading-modifying-and-writing-a-geotiff-with-gdal-in-python
        https://gis.stackexchange.com/questions/198013/numpy-to-geotiff-for-use-with-gdal
        """
        
        driver = gdal.GetDriverByName("GTiff")
        n_bands = 1
        driver_specific_options = []

        for raster_layer in self.raster_layers:
            pixels = np.copy(raster_layer.pixels)
            pixels[pixels == None]=no_data_value

            filename = os.path.join(self.dest_path, f"{slugify(raster_layer.name)}.tif")
            typecode = gdal_array.NumericTypeCodeToGDALTypeCode(pixels.dtype)
            shape = pixels.shape

            out_ds = driver.Create(filename, shape[1], shape[0], n_bands, typecode, driver_specific_options)
            band = out_ds.GetRasterBand(1)
            band.WriteArray(pixels)
            band.SetNoDataValue(no_data_value)
            band.ComputeStatistics(False)
            out_ds.FlushCache()


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')
