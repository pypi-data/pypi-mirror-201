from enum import Enum


class LayerUsage(Enum):
    LAYER_USAGE_COST = "Cost"
    LAYER_USAGE_FEATURE = "Feature"

    def __str__(self):
        return self.value
