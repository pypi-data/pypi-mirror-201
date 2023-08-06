import csv
import math
import os

import wx

from exporters.Exporter import Exporter


class CocoplanExporter(Exporter):
    def export(self):
        self.export_pu()

    def export_pu(self):
        assert len(self.cost_layers) == 1, "Exactly one cost layer must be present!"

        pu_rows = [["id", "cost", "xloc", "yloc"]]
        pvf_rows = [["feature", "pu", "amount"]]
        feature_rows = [["feature", "target", "prop", "name"]]
        edgelist_rows = [["feature", "pu1", "pu2", "value"]]

        print(self.cost_layers)
        pixels = self.cost_layers[0].pixels
        pu_id = 0

        for x in range(len(pixels)):
            for y in range(len(pixels[x])):
                pu_rows.append((pu_id, pixels[x][y], x, y))

                for feature_id, feature_layer in enumerate(self.feature_layers):
                    if feature_layer.pixels[x][y] != 0:
                        pvf_rows.append((feature_id, pu_id, feature_layer.pixels[x][y]))

                pu_id += 1

        feature_id = 0

        for feature_id, feature_layer in enumerate(self.feature_layers):
            feature_rows.append((feature_id, feature_layer.target, feature_layer.prop, feature_layer.name))

        max_feature_id = feature_id

        for graph_layer in self.graph_layers:
            cur_layer = graph_layer
            feature_id = None
            points = None

            while hasattr(cur_layer, "dependingLayer") and cur_layer.dependingLayer is not None:
                cur_layer = cur_layer.dependingLayer
                if points is None:
                    points = cur_layer.points
                if cur_layer in self.feature_layers:
                    feature_id = self.feature_layers.index(cur_layer)
                    break

            if feature_id is None:
                max_feature_id += 1
                feature_id = max_feature_id

            print(points)

            for edge in graph_layer.graph.get_edgelist():
                print(edge)
                edgelist_rows.append((feature_id, edge[0], edge[1],
                                      math.sqrt((points[0][edge[0]] - points[0][edge[1]])**2 +
                                                (points[1][edge[0]] - points[1][edge[1]])**2)))

        self.write_csv("pu.csv", pu_rows)
        self.write_csv("pvf.csv", pvf_rows)
        self.write_csv("feature.csv", feature_rows)
        self.write_csv("feature_edgelist.csv", edgelist_rows)

    def write_csv(self, filename: str, rows: list):
        filepath = os.path.join(self.dest_path, filename)

        with open(filepath, 'w', newline='') as file:
            csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerows(rows)
