import importers.GeoTIFFImporter as GeoTIFFImporter

importer_names = {importer.__name__: importer for importer in [GeoTIFFImporter.GeoTIFFImporter]}