import os.path

from layers.Parameter import Parameter
from layers.rasterLayers.RasterLayer import RasterLayer


class ImportedRasterLayer(RasterLayer):
    def __init__(self, **kwargs):
        super().__init__()
        self.parameters.extend([
            Parameter(name='importer_type', desc='Type of the imported data', parameterType=str),
            Parameter(name='rel_file_path', desc='Relative file path the data was imported from', parameterType=str),
            Parameter(name='abs_file_path', desc='Absolute file path the data was imported from', parameterType=str)
        ])
        super().update(**kwargs)
    def calculate(self):
        if self.importer is None:
            self.importer = congen.importers.importer_names[self.importer_type](layer=self)
            self.importer.import_file()
        super().calculate()

    def update_rel_path(self):
        self.rel_file_path = os.path.relpath(self.abs_file_path)