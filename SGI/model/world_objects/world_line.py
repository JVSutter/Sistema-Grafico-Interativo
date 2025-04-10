from model.world_objects.world_object import WorldObject
from view.graphical_objects.graphical_line import GraphicalLine
from view.graphical_objects.graphical_object import GraphicalObject


class WorldLine(WorldObject):
    def get_clipped_representation(self) -> None:
        graphical_line = GraphicalLine(self.viewport_points, self.color)
        return [graphical_line]
